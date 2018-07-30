#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 16:42:18 2018

@author: ralf
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test program to compare different individuals

import pandas as pd
import numpy as np
from sklearn.externals import joblib
from osgeo import gdal
import os

# read in the data
path='/datadisk/' # plase add your path to the repository here
vex=pd.read_excel(path+'Mosquito-Modeling/Climate/data/vex1.xlsx')       # 0
dac=pd.read_excel(path+'Mosquito-Modeling/Climate/data/dac1.xlsx')       # 1
gen=pd.read_excel(path+'Mosquito-Modeling/Climate/data/gen1.xlsx')       # 2
jap=pd.read_excel(path+'Mosquito-Modeling/Climate/data/jap1.xlsx')       # 3

sel=['P05','P06','P07','P14','P17','P12','P08','P06']
# sel=['P05','P11','T02','P17','T09','D07','D09','P12']
#sel=['T09','T10','T12','T13','P02','P04','P06','D10']
#sel=['T09','P05','T02','D07','T08','P11','D12','P09']
# select the training data
def get_line(data,line):
    """ read a line for one of the vextrain,gentrain,dactrain,japtrain
        and check for nan values
    """
    global sel
    L=[]
    for s in sel:
        val=data[s].iloc[line]
        if np.isnan(val):
            return None
        L.append(val)
    return L

def gen_training(size=40):
    global sel
    pdac=0.05   # sample prob for dac 
    pvex=0.25   # sample prob for vex
    pgen=0.2   # sample prob for gen 
    pjap=0.5   # use all jap data
    # define the wheel
    Xtrain=np.zeros((size,len(sel)))
    Ytrain=np.zeros(size)
    c=0
    while c<size:
        s=np.random.rand()
        test=pdac
        if(s<test):
            L=get_line(dac,np.random.randint(len(dac)))
            if(L is None):
                continue
            Ytrain[c]=0
            Xtrain[c,:]=np.array(L)
            c+=1
            continue
        test+=pvex
        if(s<test):
            L=get_line(vex,np.random.randint(len(vex)))
            if(L is None):
                continue
            Ytrain[c]=0
            Xtrain[c,:]=np.array(L)
            c+=1
            continue
        test+=pgen
        if(s<test):
            L=get_line(gen,np.random.randint(len(gen)))
            if(L is None):
                continue
            Ytrain[c]=0
            Xtrain[c,:]=np.array(L)
            c+=1
            continue
        test+=pjap
        if(s<test):
            L=get_line(jap,np.random.randint(len(jap)))
            if(L is None):
                continue
            Ytrain[c]=1
            Xtrain[c,:]=np.array(L)
            c+=1
            continue
        
    return Xtrain,Ytrain


# scale the training data 
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from xgboost import XGBClassifier
from sklearn import svm

def gen_scale(sel):
    """ generates an array XXX to fit a scaler
        using the maps from DWD based on GDAL 
    """
    XXX=np.zeros((2,len(sel))) # 2,n array to store the Min,Max
    dirs=os.listdir(path+'Mosquito-Modeling/Climate/data/') # read the filenames of the data
    print(sel)
    for i in range(len(sel)):
        print(sel[i],i)
        if('T' in sel[i]):
            for d in dirs:
                if('xml' in d):
                    continue
                if('temp' in d):
                    if(sel[i][1:]==d.split('_')[-1].split('.')[0]):
                        g=gdal.Open(path+'Mosquito-Modeling/Climate/data/'+d)
                        band=g.GetRasterBand(1)
                        #minmax=band.ComputeRasterMinMax()
                        #XXX[0,i]=minmax[0]
                        #XXX[1,i]=minmax[1]+20 
                        minmax=band.ComputeStatistics(1)
                        XXX[0,i]=minmax[2]
                        XXX[1,i]=minmax[3] 
                        
        if('P' in sel[i]):
            for d in dirs:
                if('xml' in d):
                    continue
                if('precipitation' in d):
                    if(sel[i][1:]==d.split('_')[-1].split('.')[0]):
                        g=gdal.Open(path+'Mosquito-Modeling/Climate/data/'+d)
                        band=g.GetRasterBand(1)
                        #minmax=band.ComputeRasterMinMax()
                        #XXX[0,i]=minmax[0]
                        #XXX[1,i]=minmax[1] 
                        minmax=band.ComputeStatistics(1)
                        XXX[0,i]=minmax[2]
                        XXX[1,i]=minmax[3] 
        if('D' in sel[i]):
            for d in dirs:
                if('xml' in d):
                    continue
                if('drought' in d):
                    if(sel[i][1:]==d.split('_')[-1].split('.')[0]):
                        g=gdal.Open(path+'Mosquito-Modeling/Climate/data/'+d)
                        band=g.GetRasterBand(1)
                        #minmax=band.ComputeRasterMinMax()
                        #XXX[0,i]=minmax[0]
                        #XXX[1,i]=minmax[1]  
                        minmax=band.ComputeStatistics(1)
                        XXX[0,i]=minmax[2]
                        XXX[1,i]=minmax[3] 
    return XXX
    
Xtrain,Ytrain=gen_training(4000)
XXX=gen_scale(sel)
joblib.dump(XXX, path+'Mosquito-Modeling/Climate/data/XXX.pkl')
 
for i in range(Xtrain.shape[1]):
    # Xtrain[:,i]=(Xtrain[:,i]-XXX[0,i])/(XXX[1,i]-XXX[0,i])
    Xtrain[:,i]=(Xtrain[:,i]-XXX[0,i])/XXX[1,i]
    
# define the cross validation
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
forest=XGBClassifier(learning_rate=0.01,max_depth=9,n_estimators=700)
kfold=KFold(n_splits=10)
scores = cross_val_score(forest, Xtrain, Ytrain, cv=kfold)
print(scores)
print('Accuracy: %.2f%% (%.2f%%)' % (scores.mean()*100,scores.std()*100))
clf = svm.SVC(kernel='rbf', C=1000)
scores = cross_val_score(clf, Xtrain, Ytrain, cv=kfold)
print(scores)
print('Accuracy: %.2f%% (%.2f%%)' % (scores.mean()*100,scores.std()*100))
clf = svm.SVC(kernel='rbf', C=1000, probability=True)
clf.fit(Xtrain, Ytrain)
joblib.dump(clf,path+'Mosquito-Modeling/Climate/data/clf.pkl')

