class Demo {
  constructor(modalita, modello,idPair,img1,img2) {
    this.modalita = modalita;
    this.modello = modello;
    this.idPair = idPair;
    this.img1 = img1;
    this.img2 = img2;
  }

    set_modalita(modalita){
      this.modalita =modalita;
    }
}


var dizionario = {};
dizionario["imgPair"]={};
dizionario["imgPair"]["img1"]="";
dizionario["imgPair"]["img2"]="";
dizionario["modalita"]="";
dizionario["rete"]="";
dizionario["idPair"]="";

var focus = false;

$(document).ready(function() { // quando il documento è pronto
// la pagina è caricata
// eseguo quindi le funzioni
  console.log("entrato!! :)  ");
  //oggetto



  $(".mode").on("click", function(){

            // seleziono l'oggetto item e tolgo la classe active
            $(".mode").removeClass("attiva");
            $(this).addClass("attiva");

           // gestire il contenuto del menu attivo

           var oggettoMode= $(this).data("view"); // ottengo il contenuto dell'attributo "data-view"
           console.log("E attivo",oggettoMode)

  });

  $(".rete").on("click", function(){

            // seleziono l'oggetto item e tolgo la classe active
            $(".rete").removeClass("attiva");
            $(this).addClass("attiva");

           // gestire il contenuto del menu attivo

           var oggettoRete= $(this).data("view"); // ottengo il contenuto dell'attributo "data-view"
           console.log("E attivo",oggettoRete)

  });



  $(".custom-file-input").on("change", function() {
      var fileName = $(this).val().split("\\").pop();

      $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
       var id = $(this).attr("id");
       console.log(id);
      if(id=="customFile1"){
          console.log(fileName);

          dizionario["imgPair"]["img1"]=fileName;
      }
      else if (id == "customFile2"){
          dizionario["imgPair"]["img2"]=fileName;
        }
  });





  $("#idPair").focusout(function(){

      var numId=$("#idPair").val();
      console.log(numId);
      if((numId > 1458) || (numId<0)){
        document.getElementById("idPair").value = '';
        document.getElementById("idPair").placeholder = "[0 - 1458]";
      }
      else{
        dizionario["idPair"] = numId;
      }
    });


    $("#idPair").on("focus", function(){
        $('#customFile1').siblings(".custom-file-label").addClass("selected").html("");
        $('#customFile1').siblings(".custom-file-label").addClass("selected").html("");
        $("#file1 label").html("Choose Image_1");
        $("#file2 label").html("Choose Image_2");
        dizionario["imgPair"]["img1"]="";
        dizionario["imgPair"]["img2"]="";
      });

    $("#customFile1").on("click", function(){
        document.getElementById("idPair").value = '';
        dizionario["idPair"] ="";

    });

    $("#customFile2").on("click", function(){
        document.getElementById("idPair").value = '';

    });

});

function get_cnn() {
   console.log("Cliccato cnn");
   dizionario["modalita"]="cnn";

  }

function get_snnClass() {
   console.log("Cliccato snnClass")
   dizionario["modalita"]="snnClass";
  }

function get_snnMetric() {
   console.log("Cliccato snnMetric")
   dizionario["modalita"]="snnMetric";
  }

function get_MNet() {
   console.log("Mnet");
   dizionario["rete"]="MNet";

  }

function get_ResNet() {
   console.log("ResNet");
   dizionario["rete"]="ResNet";

  }

function get_idPair(){
  console.log("idPair");
  focus= true;
  console.log(focus);
}

function start_Test() {
   console.log(dizionario);
   // controlla se i campi sono tutti riempiti
   var modalita = dizionario["modalita"];
   var rete = dizionario["rete"];
   var idPair = dizionario["idPair"];
   var imgPair = dizionario["imgPair"];
   var img1 = imgPair["img1"];
   var img2 = imgPair["img2"];
   console.log(modalita,rete,idPair,img1,img2);

   var errore = "";
   if(modalita ==""){
      errore = errore+"Choose Mode of testing "+"\n";
   }
   if(rete ==""){
    errore = errore+"Choose Neural Network"+"\n";
   }
   if((idPair=="")){
      if((img1=="")||(img2=="")){
        errore = errore+"Choose idPair or Image"+"\n";
      }
   }
   console.log(errore);
   if(errore!=""){
    alert(errore);
    }else{
    console.log("Send the request");
    const url = 'http://127.0.0.1:5000/hello'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        console.log(json);
        document.getElementById("demo").innerHTML = JSON.stringify(json)
    })



        }
  }

function clickCheck(){
  console.log("Click");

}
