import json
from Demo import Demo
import torch
def processModelById(mode, network, idPair):
    etichetta_predetta=""
    path_img_1=""
    path_img_2=""
    resize=100
    if((mode=="cnn") and (network=="ResNet")):
        resize=256

    idPair = int(idPair)
    demo_obj = Demo( resize)
    demo_obj.readDataset()
    demo_obj.controlPair(idPair)
    demo_obj.read_normalize()
    dizionario = demo_obj.getitem(idPair)
    # dizionario contiene
    # {'image_1' : img_tensor_1, 'label_1':self.label_img1, 'image_2' : img_tensor_2, 'label_2': self.label_img2, 'label_lij':self.label_ij}

#-------------CLASSFIZICAZIONE------ A SINGOLA IMMAGINE---
    if(mode=="cnn"):
        if(network == "MNet"):
            model = torch.load("class_2_44.pth")
            demo_obj.test_demo_order_manual(dizionario, model)

        elif(network == "ResNet"):
            model = torch.load("class_1_19.pth")

            demo_obj.test_demo_order_manual(dizionario, model)

        etichetta_predetta={"pred_Pair":demo_obj.preds,"path_img_1":demo_obj.path_1,"path_img_2":demo_obj.path_2,"class_1":demo_obj.preds_img_1,"class_2":demo_obj.preds_img_2,"real":demo_obj.real}
        return etichetta_predetta
#------------SNN------- CROSS ENTROPY--------------------
    elif(mode == "snnClass"):
        if(network == "ResNet"):
            model = torch.load("modello5_v5.pth")
            demo_obj.test_demo(dizionario, model)

        elif(network == "MNet"):
            model = torch.load("modello5_v7_17.pth")
            demo_obj.test_demo(dizionario, model)

#----------SNN---------SINGLE MARGINE-------------------
    elif(mode == "snnMetric"):
        soglia=""
        if(network == "ResNet"):
            model = torch.load("modello6_v2_6.pth")
            soglia = 0.92

            demo_obj.test_demo_single_margine(dizionario, model,soglia)


    etichetta_predetta = {"pred_Pair":demo_obj.preds, "path_img_1":demo_obj.path_1,"path_img_2":demo_obj.path_2,"unita1":demo_obj.label_img1,"unita2":demo_obj.label_img2,"real":demo_obj.real }
    return etichetta_predetta
