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

var disabilitaMNet = function(){
  document.getElementById("MNet").disabled = true;
  document.getElementById("MNet").checked = false;
  console.log("disabilita MNet");
}

var abilitaMNet = function(){
  console.log("abilita MNet");
  document.getElementById("MNet").disabled = false;
  console.log("abilita MNet");
}

var dizionario = {};
dizionario["imgPair"]={};
dizionario["imgPair"]["img1"]="";
dizionario["imgPair"]["img2"]="";
dizionario["modalita"]="";
dizionario["rete"]="";
dizionario["idPair"]="";
dizionario["format1"]=""
dizionario["format2"]=""
var focus = false;

$(document).ready(function() { // quando il documento è pronto
// la pagina è caricata
// eseguo quindi le funzioni
  console.log("entrato!!   ");
  //svuota();
  //oggetto


/*
  $('form').on('submit',function(event){
    $.ajax({
      data:{ mode:dizionario['modalita'],
             network :dizionario['rete'],
             idpair :dizionario['idPair']
           },
           type:'POST',
           url:'/'
    })
    .done(function(data){
      if(data.error){
        $('#errorAlert').text(data.error).show();

      }
      else{

        $('#errorAlert').hide();
        label = data.label;
        img1 = data.img1;
        img2 = data.img2;
        console.log(label,img1,img2);

        $.ajax({
          data:{
                  go:"result"
               },
               type:'GET',
               url:'/'
        });


      }
    });

    event.preventDefault();

  });*/




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

  $("#homeClick").on("click", function(){
      console.log("cliccato");
  });


  $(".custom-file-input").on("change", function() {
      var pathFile =$(this).val();
      console.log(pathFile);
      var fileName = $(this).val().split("\\").pop();

      $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
       var id = $(this).attr("id");

       console.log(id);
      if(id=="customFile1"){
          console.log(fileName);
          var input = document.getElementById(id);
          //koala.jpg, koala.JPG substring(index) lastIndexOf('a') koala.1.jpg
          var ext= fileName.substring(fileName.lastIndexOf('.')+1).toLowerCase();
          console.log("Estensione1",ext);
          if ((ext != 'jpg')){
              console.log("errore");
              dizionario["format1"]="error";
            }else{
              console.log("noerrore");
              dizionario["format1"]="";
            }
          dizionario["imgPair"]["img1"]=fileName;
      }
      else if (id == "customFile2"){
        var input = document.getElementById(id);
        //koala.jpg, koala.JPG substring(index) lastIndexOf('a') koala.1.jpg
        var ext= fileName.substring(fileName.lastIndexOf('.')+1).toLowerCase();
        console.log("Estensione2",ext);
        if ((ext != 'jpg')){
            console.log("errore");
            dizionario["format2"]="error";
          }else{

            console.log("noerrore");
            dizionario["format2"]="";
          }
          dizionario["imgPair"]["img2"]=fileName;
        }
  });


$("#snnMetric" ).on( "click", disabilitaMNet );
$("#snnClass").on("click",abilitaMNet);
$("#cnn").on("click",abilitaMNet);




  $("#idPair").focusout(function(){

      var numId=$("#idPair").val();
      console.log(numId);
      if((numId > 1458) || (numId<0)){
        document.getElementById("idPair").value ="";
        document.getElementById("idPair").placeholder = "[0 - 13824]";
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
        document.getElementById("idPair").value ="";
        dizionario["idPair"] ="";
        document.getElementById("idPair").placeholder = "[0 - 13824]";
    });

    $("#customFile2").on("click", function(){
        document.getElementById("idPair").value ="";
        dizionario["idPair"] ="";
        document.getElementById("idPair").placeholder = "[0 - 13824]";
    });



});
function svuota(){

  $('#customFile1').val(null);
  $('#customFile2').val(null);
  //$('#customFile1').siblings(".custom-file-label").addClass("selected").html('');
  //$('#customFile2').siblings(".custom-file-label").addClass("selected").html('');
  $("#file1 label").html("Chose Image_1");
  $("#file2 label").html("Chose Image_2");
  $("input.form-check-input ").attr('checked', false);
  dizionario["imgPair"]={};
  dizionario["imgPair"]["img1"]="";
  dizionario["imgPair"]["img2"]="";
  dizionario["modalita"]="";
  dizionario["rete"]="";

  document.getElementById("idPair").value="";
  dizionario["idPair"]="";
  document.getElementById("idPair").placeholder ="[0 - 13824]";

}

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
   $("MNet").attr("disabled", true);
   console.log("disabilita MNet");
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

  if(document.getElementById('cnn').checked) {
    dizionario["modalita"]="cnn";
  }else if(document.getElementById('snnClass').checked) {
    dizionario["modalita"]="snnClass";
  }else if(document.getElementById('snnMetric').checked){
    // disabilitare MNet

    dizionario["modalita"]="snnMetric";
  }else{
    dizionario["modalita"]="";
  }


  if(document.getElementById('MNet').checked) {
    dizionario["rete"]="MNet";
  }else if(document.getElementById('ResNet').checked) {
    dizionario["rete"]="ResNet";
  }else{
    dizionario["rete"]="";
  }

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
      }else{
        var format1 = dizionario["format1"];
        var format2 = dizionario["format2"];
        if((format1=="error")||(format2=="error")){
          errore= errore + "Format Files are not supported, load format 'jpg'"+"\n";
        }
      }
   }
   console.log(errore);
   if(errore!=""){
    svuota();
    alert(errore);

    }else{
    console.log("Send the request");


    span=document.createElement("span");
    span.setAttribute("class","spinner-grow spinner-grow-sm");
    span.setAttribute("role","status")
    span.setAttribute("aria-hidden","true")
    bottone=document.getElementById('bottoneTest');

    //bottone.disabled = true;

    $('#bottoneTest').empty();
    $('#bottoneTest').append(span);
    $('#bottoneTest').append("<span style=\"font-size:0.9rem\">Testing...</span>");
    $('#')

    }
  }

function clickCheck(){
  console.log("Click");

}

function edit()
{     console.log("Svuota img");
      var img1 = document.getElementById("#boxImg1 img");
      var perc = img.getAttribute("src");
      console.log(perc);
      img1.setAttribute("src","");

      var img2 = document.getElementById("#boxImg2 img");
      img2.setAttribute("src","");

      var img1 = document.getElementById("#boxImg1 img");

      var imgP = img1.getAttribute("src");
      console.log("Percorso dopo la modifica",imgP);




}
