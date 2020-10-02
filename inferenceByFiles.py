import json
from Demo import Demo
import torch
import os
import glob

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def uploadFiles(files, img1, img2):
    #target = os.path.join(APP_ROOT, 'images/')
    target = os.path.join(APP_ROOT, 'static/Upload')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Elimina file dalla cartella".format(target))
        filesD = glob.glob(target+'/*')

        for f in filesD:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))

    file1=files["img1"]
    file2=files["img2"]
    print("Files",file1,file2)
    destination1 = "/".join([target, file1])
    destination2 = "/".join([target, file2])
    print ("Accept incoming file1, file2:", file1, file2)
    print ("Save it to:", destination1, destination2)
    img1.save(destination1)
    img2.save(destination2)



def processModelByFile(mode, network,path_img_1,path_img_2):
    etichetta_predetta=""
    print("Percorso file1", path_img_1)
    print("Percorso file2", path_img_2)
    resize=100

    if((network=="ResNet")and(mode=="cnn")):
        resize=256

    print("Resize",resize)
    demo_obj = Demo(resize)
    demo_obj.read_normalize()
    dizionario = demo_obj.tranformFile(path_img_1,path_img_2)
    model=""
#-------------CLASSFIZICAZIONE------ A SINGOLA IMMAGINE---
    print("Inference by FILE classificazione singola")
    if(mode=="cnn"):
        if(network == "MNet"):
            model = torch.load("class_2_44.pth")
        elif(network == "ResNet"):
            model = torch.load("class_1_19.pth")

        demo_obj.test_demo_order_manual(dizionario, model)
        etichetta_predetta={"class_1":demo_obj.preds_img_1,"class_2":demo_obj.preds_img_2,"pred_Pair":demo_obj.preds}
        return etichetta_predetta

#------------SNN------- CROSS ENTROPY--------------------
    elif(mode == "snnClass"):
        if(network == "ResNet"):
            model = torch.load("modello5_v5.pth")

        elif(network == "MNet"):
            model = torch.load("modello5_v7_17.pth")

        demo_obj.test_demo(dizionario, model)

#----------SNN---------SINGLE MARGINE-------------------
    elif(mode == "snnMetric"):
        soglia=""
        if(network == "ResNet"):
            model = torch.load("modello6_v2_6.pth")
            soglia = 0.92

        dist = demo_obj.test_demo_single_margine(dizionario, model,soglia)

    etichetta_predetta = {"pred_Pair":demo_obj.preds}
    return etichetta_predetta
