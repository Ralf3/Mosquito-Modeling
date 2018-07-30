#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test program to compare different individuals

import pandas as pd
import numpy as np
from sklearn.externals import joblib
import pylab as plt
import operator
import matplotlib

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
    for i in range(3,49):
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
    Xtrain=np.zeros((size,49-3))
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
    
def gen_testing(size=40):
    pdac=0.05   # sample prob for dac 
    pvex=0.25   # sample prob for vex
    pgen=0.2   # sample prob for gen 
    pjap=0.5   # use all jap data
    # define the wheel
    Xtest=np.zeros((size,49-3))
    Ytest=np.zeros(size)
    c=0
    while c<size:
        s=np.random.rand()
        test=pdac
        if(s<test):
            L=get_line(dactrain,np.random.randint(len(dactest)))
            if(L is None):
                continue
            Ytest[c]=0
            Xtest[c,:]=np.array(L)
            c+=1
            continue
        test+=pvex
        if(s<test):
            L=get_line(vextrain,np.random.randint(len(vextest)))
            if(L is None):
                continue
            Ytest[c]=0
            Xtest[c,:]=np.array(L)
            c+=1
            continue
        test+=pgen
        if(s<test):
            L=get_line(gentrain,np.random.randint(len(gentest)))
            if(L is None):
                continue
            Ytest[c]=0
            Xtest[c,:]=np.array(L)
            c+=1
            continue
        test+=pjap
        if(s<test):
            L=get_line(japtrain,np.random.randint(len(japtest)))
            if(L is None):
                continue
            Ytest[c]=1
            Xtest[c,:]=np.array(L)
            c+=1
            continue
        
    return Xtest,Ytest
        

# scale the training data 
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

Xtrain,Ytrain=gen_training(4000)
scaler = StandardScaler()
scaler.fit(Xtrain)
Xtrain=scaler.transform(Xtrain)

forest=XGBClassifier(learning_rate=0.01,max_depth=9,n_estimators=700)
model=forest.fit(Xtrain, Ytrain)
# plot_importance(model)
names=vextrain.columns[3:-1]
fd={n:v for n,v in zip(names,model.feature_importances_)}
fds=sorted(fd.items(), key=operator.itemgetter(1),reverse=True)
n=[]
v=[]
k=1
s=0
for i in fds:
    n.append(i[0])
    v.append(i[1])
    s+=i[1]
    ss="%d & %s & %1.5f & %1.5f" % (k,i[0],i[1],s)
    print(ss)
    k+=1
# print the latex code
matplotlib.rcParams.update({'font.size': 16})    
fig, ax = plt.subplots(figsize=(30,30))
#ax.yaxis.set_major_formatter(formatter)
x=range(len(n))
plt.bar(x,v)
plt.xticks(x, n)
plt.show()

# tests 
