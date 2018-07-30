#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:55:40 2018

@author: antje
"""

import pandas as pd

''' read the files from the German weather service 
    that are the most close to the research areas  R0, R1 and R2; '''
    
path = '/datadisk/Mosquito-Modeling/SIR/data/'

#R0=space_simu.region(landscape[1000:1250,4500:4750]) # R0: region without mosquitoes 
#R1=space_simu.region(landscape[4800:5050,700:950])   # R1: high mosquito region
#R2=space_simu.region(landscape[2900:3150,2200:2450]) # R2: no spread region
r0 = pd.read_csv(path+'produkt_tu_stunde_19730101_20171231_05009.txt',
                 delimiter = ';',
                 delim_whitespace=False
                 )

r1 = pd.read_csv(path+'produkt_tu_stunde_20040901_20171231_03490.txt', 
                 delimiter= ';',
                 delim_whitespace=False
                 )

r2 = pd.read_csv(path+'produkt_tu_stunde_20040701_20171231_00294.txt', 
                 delimiter=';',
                 delim_whitespace=False
                 )

class Weather():
    """ This class returns the weather conditions (mean daily temperature)
    at a given day """
    
    def __init__(self,region,datum):
        """ weather is initialized with the station r0,r1,r2
            and with a starting date 
        """
        self.date=datum
        self.region=region
        self.index=self.region[(self.region.MESS_DATUM.astype('str')).str.startswith(self.date)].index[0]
        
    def next(self):
        res=self.region.iloc[self.index:self.index+24]
        s=0
        k=0
        for x in res['TT_TU']:
            if(x==-999):
                continue
            s+=x
            k+=1
        self.index+=24
        if k!=0:
            return s/k
        return -999
    
import pylab as plt
w=Weather(r1,'20120101')
TX=[]
for i in range(365*5):
    TX.append(w.next())
plt.plot(TX[0:365])
plt.grid()
plt.xlabel('t [d]')
plt.ylabel('T [grd]')
plt.title('Mean temperature from 2010')
plt.show()