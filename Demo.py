# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 00:28:01 2020

@author: rosaz
"""
import sys
import os
import json
import torch
import pandas as pd
from os.path import join
from PIL import Image
from torchvision import transforms
from torch.utils import data
from matplotlib import pyplot as plt
from torch.nn import functional as F
class Demo(data.Dataset):

    def __init__(self, resize):
        self.resize = resize

    def readDataset(self):
        self.path = "Dataset"
        self.data = pd.read_csv("static/Dataset/Pair_test.csv")


    def controlPair(self,id_Pair):
        print(type(id_Pair))
        print("Control id Pair...")
        try:
            with open("static/Dataset/Pair_test.csv") as f:
                next(f)
                self.sumTrain = sum(1 for line in f)
                if (id_Pair>= 0) & (id_Pair<self.sumTrain):
                    print(self.sumTrain)
                    print("Ok")
                else:
                    print("Non esiste id Pair %d, id max pair %d" %(id_Pair, self.sumTrain-1))

                    exit(0)
        except IOError as e:
            sys.stderr.write("fatal error, try run --create datasetPair")
            exit(0)

    def read_normalize(self):
           mean = [0.5952371499212669,0.5766087426163746,0.6113024027742164]
           self.mean = tuple(mean)
           print(self.mean)
           dev_std = [0.09794762927822352, 0.10893689120546401,0.1402488281204596]
           self.dev_std = tuple(dev_std)
           print(self.dev_std)
           self.transform = transforms.Compose([transforms.Resize(self.resize),transforms.ToTensor(), transforms.Normalize(self.mean,self.dev_std)])


    def getitem(self,i):

        img1_path = self.data.iloc[i]['path_img_1']
        label_1 = self.data.iloc[i]['label_img_1']
        self.path_1 = img1_path
        img2_path = self.data.iloc[i]['path_img_2']
        label_2 = self.data.iloc[i]['label_img_2']
        self.path_2 = img2_path
        label_pair = self.data.iloc[i]['lij']

        self.img1_photo = Image.open(join("static/Dataset//",img1_path)).convert('RGB')
        self.img2_photo = Image.open(join("static/Dataset//",img2_path)).convert('RGB')

        self.label_img1 = int(label_1)
        self.label_img2 = int(label_2)
        self.label_ij =  int(label_pair)

        #se la trasfromazione è definita, applichiamola all'immagine
        if self.transform is not None:

            img_tensor_1 = self.transform(self.img1_photo)
            img_tensor_2 = self.transform(self.img2_photo)

        return {'image_1' : img_tensor_1, 'label_1':self.label_img1, 'image_2' : img_tensor_2, 'label_2': self.label_img2, 'label_lij':self.label_ij}

    def tranformFile(self,path_img_1,path_img_2):
        self.img1_photo = Image.open(path_img_1).convert('RGB')
        self.img2_photo = Image.open(path_img_2).convert('RGB')
        #se la trasfromazione è definita, applichiamola all'immagine
        if self.transform is not None:

            img_tensor_1 = self.transform(self.img1_photo)
            img_tensor_2 = self.transform(self.img2_photo)

        return {'image_1' : img_tensor_1, 'label_1':"image_1", 'image_2' : img_tensor_2, 'label_2': "image_2", 'label_lij':100}


    def test_demo_order_manual(self,dizionario, model):
        #print(dizionario)
        self.preds_img_1=""
        self.preds_img_2=""
        self.preds=""
        self.real=""
        input_1 = dizionario['image_1'].unsqueeze(0)
        input_2 = dizionario['image_2'].unsqueeze(0)
        print(dizionario['image_1'])
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)



        class_img1 = model(input_1.to(device))#img 1
        class_img2 = model(input_2.to(device))#img2




        self.preds_img_1 = class_img1.to('cpu').max(1)[1].item()
        self.preds_img_2 = class_img2.to('cpu').max(1)[1].item()

        if(self.preds_img_1 <= self.preds_img_2):
            self.preds = 0
        else:
            self.preds = 1

        print("Reale ",dizionario['label_lij'])
        self.real = dizionario['label_lij']
        print("Predette <= ",self.preds)
        print("Classe predetta img_1",self.preds_img_1)
        print("Classe predetta img_2", self.preds_img_2)





    def test_demo(self,dizionario, model):
        #print(dizionario)
        self.preds=""
        self.real=""
        input_1 = dizionario['image_1'].unsqueeze(0)
        input_2 = dizionario['image_2'].unsqueeze(0)
        print(dizionario['image_1'])
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)



        phi_i = model(input_1.to(device))#img 1
        phi_j = model(input_2.to(device))#img2

        print(phi_i)
        f = torch.cat((phi_i,phi_j),1)

        output = model.fc2(f)
        self.preds = output.to('cpu').max(1)[1].item()


        print("Reale ",dizionario['label_lij'])
        print("Predette ",self.preds)
        self.real= dizionario['label_lij']


    def test_demo_single_margine(self,dizionario, model,soglia):
        #print(dizionario)
        print("DEMO SINGLE MARGIN- RESNET ")
        self.preds=""
        self.real=""
        self.dist=""
        input_1 = dizionario['image_1'].unsqueeze(0)
        input_2 = dizionario['image_2'].unsqueeze(0)
        print(dizionario['image_1'])
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)

        phi_i = model(input_1.to(device))#img 1
        phi_j = model(input_2.to(device))#img2

        dist = F.pairwise_distance(phi_i, phi_j)
        dist = dist.cpu()
        dist = dist.item()
        print("DISTANZE ",dist)
        if dist<= soglia:
            self.preds=0
        else:
            self.preds=1

        self.real = dizionario['label_lij']
        print("Etichetta reale", self.real)
        self.dist=dist


    def plottare(self, dist=None):

        plt.figure(figsize=(16,4))
        if self.preds == 0:
            stringa = "True"
        else:
            stringa = "False"

        if dist is not None:
            titolo= str(self.label_img1+1)+' <= '+str(self.label_img2+1)+" : "
            distanza='{:.3f}'.format(dist)
            plt.suptitle(titolo+stringa+"  \n distanza:"+distanza, fontsize=16)
        else:
            titolo= str(self.label_img1+1)+' <= '+str(self.label_img2+1)+" : "
            plt.suptitle(titolo+stringa, fontsize=16)

        plt.subplot(1,2,1)
        plt.xlabel('Img_1')
        plt.imshow(self.img1_photo)
        plt.title('Units:'+str(self.label_img1+1))
        plt.subplot(1,2,2)
        plt.xlabel('Img_2')
        plt.imshow(self.img2_photo)
        plt.title('Units:'+str(self.label_img2+1))
        plt.show()

    def norm(self,im):
        im = im-im.min()
        return im/im.max()
