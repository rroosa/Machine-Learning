import os
import json
from flask import Flask, render_template, request, redirect, jsonify
import datetime

from inferenceById import processModelById
from inferenceByFiles import uploadFiles, processModelByFile
from commons import format_class_name


app = Flask(__name__)

accuracy={ "cnn":{"MNet":0.9857,"ResNet":0.9995}, "snnClass":{"MNet":0.9444 , "ResNet":0.9991}, "snnMetric":{"MNet":0 , "ResNet":0.6975}}



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        #----- se la richiesta è vuota reindirizza in index.HTML
        list = request.form.getlist('mode')
        print("mode",list)
        if not list:
            print("Richiesta vuota")
            return render_template("index.html")

        mode=""
        network=""
        nomeMode = ""
        #--------- MODALITA------
        print(request.form.getlist('mode'))
        option =request.form.getlist('mode')[0];
        print("Opzione",option);
        if (option == "cnn"):
            mode=mode+"cnn"
            nomeMode= "CNN - single classification "
        elif (option == "snnClass"):
            mode=mode+"snnClass"
            nomeMode = "SNN - Classification of Pair"
        elif (option == "snnMetric"):
            mode=mode+"snnMetric"
            nomeMode= "SNN - Metric Learning, single margin"

        #-------NETWORK------------
        print(request.form.get('network'))
        rete =request.form.getlist('network')[0];
        print("Network",rete);
        if (rete == "MNet"):
            network=network+"MNet"
        elif (rete == "ResNet"):
            network=network+"ResNet"
        #---- get accuracy----------
        valueAcc = accuracy[option][rete]
        #------IDPAIR-----or--- FILES--------
        fileImg = {}
        idPair = request.form["idpair"]
        if idPair !="":
            print("Id Pair", idPair)
            fileImg["idPair"]=idPair
        else:
            f = request.files.get('filename1')
            print(request.files.get("filename1"))
            print(request.files.get("filename2"))
            img1 = request.files.get("filename1")
            print("Image_1", img1.filename)
            img2 = request.files.get("filename2")
            print("Image_2",img2.filename)

            if(img1.filename == img2.filename ):
                nameImg2 = "0"+img2.filename
                obj ={"img1":img1.filename, "img2":nameImg2 }
            else:
                obj ={"img1":img1.filename, "img2":img2.filename }


            fileImg["imgFile"]=obj

        y = json.dumps(fileImg)

        #----------- gestione richiesta--ID--------
        if not(fileImg.get("idPair") is None):
            print("Gestione richiesta per ID")
            id = fileImg["idPair"]
            print("Input ottenuto",mode,network,id)
            dizionario = processModelById(mode, network, id)
            path_img_1 = dizionario["path_img_1"]
            path_img_2 = dizionario["path_img_2"]
            path_img_1= "/static/Dataset/"+path_img_1
            path_img_2= "/static/Dataset/"+path_img_2
            etichetta_predetta = dizionario["pred_Pair"]
            print("Output",etichetta_predetta,path_img_1,path_img_2)
            colorPred=""
            if(etichetta_predetta==0):
                etichetta_predetta="True"
                colorPred="color:#e33617"
            elif(etichetta_predetta==1):
                etichetta_predetta="False"
                colorPred="color:#002bff"
            unita1=""
            unita2=""
            testo=""
            real="___"
            colorReal=""
            real = dizionario["real"]
            if(real == 1):
                real = "False"
                colorReal="color:#002bff"
            else:
                real = "True"
                colorReal="color:#e33617"

                #----------gestione nel caso di classif. singola img
            if not(dizionario.get("class_1") is None):
                print("Gestione by ID classificazione singola")
                unita1 = str(dizionario["class_1"]+1)
                unita2 = str(dizionario["class_2"]+1)
                testo = "Unit predicted"


            else:
                #------- gestione di siamese ---------
                print("Gestione by ID classificazione simanese")
                unita1 = str(dizionario["unita1"]+1)
                unita2 = str(dizionario["unita2"]+1)

            return render_template("result.html", label=etichetta_predetta,img1=path_img_1,img2=path_img_2, unita1=unita1, unita2=unita2, nomeMode=nomeMode, network=network, testo=testo, accuracy=valueAcc, real= real,colorReal=colorReal,colorPred=colorPred)

        #-----------gestione richiesta--FILES----------

        elif not(fileImg.get("imgFile") is None):
            path_img_1=""
            path_img_2=""

            uploadFiles(fileImg["imgFile"], img1, img2)
            path_img_1= "static/Upload/"+fileImg["imgFile"]["img1"]
            path_img_2= "static/Upload/"+fileImg["imgFile"]["img2"]
            print("File prelevato da static ",path_img_1,path_img_2 )
            dizionario = processModelByFile(mode, network,path_img_1,path_img_2)

            pred_Pair = dizionario["pred_Pair"]
            if(pred_Pair==0):
                label="True"
            elif(pred_Pair==1):
                label="False"

            unita1=""
            unita2=""
            testo=""
            real="___"
            path_new_1=""
            path_new_2=""
            colorPred="color:#c16900"
            #---------gestione nel caso di classificazione. singola img
            if not(dizionario.get("class_1") is None):
                print("Gestione by FILE classificazione singola")
                unita1 = str(dizionario["class_1"]+1)
                unita2 = str(dizionario["class_2"]+1)
                testo = "Unit predicted"
            else:
                #------ gestione di siamnese----------
                print("Gestione by FILE classificazione simanese")
                unita1 = "Image_1"
                unita2 = "Image_2"

            timestamp = str(datetime.datetime.now())

            path_new_1 = "/"+path_img_1+'?_=' + timestamp
            path_new_2 = "/"+path_img_2+'?_=' + timestamp
            return render_template("result.html", label=label,img1=path_new_1,img2=path_new_2, unita1=unita1, unita2=unita2, nomeMode=nomeMode, network=network,testo=testo, accuracy=valueAcc, real=real,colorPred=colorPred)

    print("Ritorna nella pagina iniziale")
    return render_template('index.html')

@app.route('/home')
def home():
      return render_template("index.html")






if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
