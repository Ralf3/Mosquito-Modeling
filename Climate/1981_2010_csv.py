#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test program to compare different individuals

import pandas as pd
import numpy as np
import sys
from sklearn.externals import joblib
import random
import array
import pylab as plt
import pprint

# read in the data
path='/datadisk/'
vex=pd.read_excel(path+'Mosquito-Modeling/Climate/data/vex1.xlsx')       # 0
dac=pd.read_excel(path+'Mosquito-Modeling/Climate/data/dac1.xlsx')       # 1
gen=pd.read_excel(path+'Mosquito-Modeling/Climate/data/gen1.xlsx')       # 2
jap=pd.read_excel(path+'Mosquito-Modeling/Climate/data/jap1.xlsx')       # 3

# select the training
vextrain=vex[vex.year<2018]
gentrain=gen[gen.year<2018]
japtrain=jap[jap.year<2018]
dactrain=dac[dac.year<2018]

# selet the testing
vextest=vex[vex.year==2017]
gentest=gen[gen.year==2017]
japtest=jap[jap.year==2017]
dactest=dac[dac.year==2017]


# select the used species
used=[vextrain,gentrain,dactrain,japtrain]
tused=[vextest,gentest,dactest,japtest]

# select the training data
def get_line(data,line):
    """ read a line for one of the vextrain,gentrain,dactrain,japtrain
        and check for nan values
    """
    L=[]
    for i in range(3,11):
        val=data.iloc[line,i]
        if np.isnan(val):
            return None
        L.append(val)
    return L
    
def gen_training(size=40):
    pdac=0.05   # sample prob for dac 
    pvex=0.25   # sample prob for vex
    pgen=0.2   # sample prob for gen 
    pjap=0.5   # use all jap data
    # define the wheel
    Xtrain=np.zeros((size,8))
    Ytrain=np.zeros(size)
    c=0
    while c<size:
        s=np.random.rand()
        test=pdac
        if(s<test):
            L=get_line(dactrain,np.random.randint(len(dactrain)))
            if(L is None):
                continue
            Ytrain[c]=0
            Xtrain[c,:]=np.array(L)
            c+=1
            continue
        test+=pvex
        if(s<test):
            L=get_line(vextrain,np.random.randint(len(vextrain)))
            if(L is None):
                continue
            Ytrain[c]=0
            Xtrain[c,:]=np.array(L)
            c+=1
            continue
        test+=pgen
        if(s<test):
            L=get_line(gentrain,np.random.randint(len(gentrain)))
            if(L is None):
                continue
            Ytrain[c]=0
            Xtrain[c,:]=np.array(L)
            c+=1
            continue
        test+=pjap
        if(s<test):
            L=get_line(japtrain,np.random.randint(len(japtrain)))
            if(L is None):
                continue
            Ytrain[c]=1
            Xtrain[c,:]=np.array(L)
            c+=1
            continue
        
    return Xtrain,Ytrain
    
# scale the training data 
from sklearn.preprocessing import StandardScaler
Xtrain,Ytrain=gen_training(4000)
scaler = StandardScaler()
scaler.fit(Xtrain)
Xtrain=scaler.transform(Xtrain)

# define the cross validation
from sklearn.model_selection import cross_val_score
from sklearn import svm
clf = svm.SVC(kernel='rbf', C=1, probability=True)
scores = cross_val_score(clf, Xtrain, Ytrain, cv=10)
print(scores)
print('Accuracy: %.2f%% (%.2f%%)' % (scores.mean()*100,scores.std()*100))
filename = 'svm.save'
joblib.dump(clf, filename)
# test the model
clf.fit(Xtrain, Ytrain)
Xtest=np.zeros((len(japtest),8))
for i in range(len(japtest)):
    line=get_line(japtest,i)
    if(line is not None):
        Xtest[i,:]=line
Xtest=scaler.transform(Xtest)
res=clf.predict_proba(Xtest)
plt.hist(res[:,1])
plt.show()