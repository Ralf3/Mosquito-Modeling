#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:55:40 2018

@author: antje
"""

import pandas as pd
from datetime import date, timedelta
import pylab as plt

''' read the files from the German weather service 
    that are the most close to the research areas  R0, R1 and R2; '''
    
path = '/datadisk/Mosquito-Modeling/SIR/data/'

#R0=space_simu.region(landscape[1000:1250,4500:4750]) # R0: region without mosquitoes 
#R1=space_simu.region(landscape[4800:5050,700:950])   # R1: high mosquito region
#R2=space_simu.region(landscape[2900:3150,2200:2450]) # R2: no spread region
r0 = pd.read_csv(path+'produkt_tu_stunde_19730101_20171231_05009.txt',
                 delimiter = ';',
                 delim_whitespace=False,
                 na_values= -999
                 )

r1 = pd.read_csv(path+'produkt_tu_stunde_20040901_20171231_03490.txt', 
                 delimiter= ';',
                 delim_whitespace=False,
                 na_values= -999
                 )

r2 = pd.read_csv(path+'produkt_tu_stunde_20040701_20171231_00294.txt', 
                 delimiter=';',
                 delim_whitespace=False,
                 na_values= -999
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
                
    def next(self):
       """ uses the date start for one day selection """
       start_time="%04d%02d%02d00" % (self.date.year,self.date.month,self.date.day)
       start_time=int(start_time)
       self.date=self.date+timedelta(1)
       end_time="%04d%02d%02d00" % (self.date.year,self.date.month,self.date.day)
       end_time=int(end_time)
       mask=(self.region['MESS_DATUM']>=start_time) &\
             (self.region['MESS_DATUM']<end_time) &\
             (pd.notna(self.region['TT_TU']))
       return self.region[mask]['TT_TU'].mean()

w=Weather(r0,date(2011,1,1))
TX=[]
for i in range(365*6):
    TX.append(w.next())
    # print(i,TX[i])
print(len(TX))
plt.plot(TX[5*365:6*365])
plt.grid()
plt.xlabel('t [d]')
plt.ylabel('T [grd]')
plt.title('Mean temperature')
plt.show()

