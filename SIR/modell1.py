#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:32:57 2018

@author: ralf
"""

""" model combines the space simu with the time simu by stepsize=1
"""
import sys
path='/datadisk/'
sys.path.append(path+'Mosquito-Modeling/SIR')
import space_simu 
import time_simu 
from osgeo import gdal
import numpy as np
import Read_Temperature as RT
from datetime import date, timedelta

# load the space after 
# read a ascii_file using gdal
def read_ascii(filename):
    g=gdal.Open(filename)
    return g.ReadAsArray()

# read the FuzzyResult as landscape
landscape=read_ascii(path+'Mosquito-Modeling/SIR/data/FuzzyResult_Version3_1981_2010.asc')
R0=space_simu.region(landscape[1000:1250,4500:4750]) # R0: region without mosquitoes 
R1=space_simu.region(landscape[4800:5050,700:950])   # R1: high mosquito region
R2=space_simu.region(landscape[2900:3150,2200:2450]) # R2: no spread region

#R.load_region(path+'region1.npy')
# load the mosquitoes as list of objects
#M=space_simu.mosquitoes(R2)
#M.load_mosquitoes(path+'mosquitoes1.pkl')
# R2.show()

#define the carrying capcity of the landscape for mosquitoes
# len(M.m) = 
#cp=100 # carrining capacity 
#
#T_month=np.array([4.0,3.0,7.2,9.9,17.7,17.4,21.1,22.0,14.0,13.6,4.0,-1.6, 
#                  1.5,6.4,7.2,10.3,18.1,20.9,22.0,21.2,15.8,9.7,7.9,-0.2,
#                  -0.2,-1.6,6.8,10.5,18.4,23.1,22.3,24.5,16.7,8.6,7.3,1.5,
#                  -0.7,3.4,4.9,12.5,14.7,18.2,20.7,21.5,15.9,11.8,6.3,1.8,
#                  2.4,-0.4,4.7,12.1,16.5,19.5,21.2,19.1,16.8,10.9,4.5,0.2])
#period=np.arange(T_month.shape[0])  # for interpolation
#f = interp1d(period, T_month)
#tx=np.arange(30*(T_month.shape[0]-1))

""" save the locations of the mosquitoes and the infected as matrix for the 
    highest values
"""

class SIMU():
    """ SIMU controls the simulation:
        the temperatur as input
        the time steps as input
        the output can be the model variables:  
        LM,SM,EM,IM,SB,EB,IB,RB,DB
    """
    def __init__(self,lat,M):
        self.sir=time_simu.SIR(lat)   # start at a latitude
        self.space=M
        self.sir.set_init_conditions(sm=0.50, lm=0.5, sb=0.5)
        if(np.mean(self.space.R.R)>0.6):
            self.sir.KM=100.0  # set the carrying capacity
        else:
            self.sir.KM=100*np.mean(self.space.R.R)
        self.factor=0.01   # 100/0.01 = 100000     
        self.log_file=open(path+'/Mosquito-Modeling/SIR/results/log.csv','w')
        s="t mosquitoes infected\n"
        self.log_file.write(s)
        self.highestm=1    # start with an asumption 
        self.highesti=1    # start with an asumption 
        self.m=None
        self.inf=None
    def time_step(self,t,tx,yd):
        """ run one step using the temperatur tx and the yearday yd as inputs """
        #sir.SM=(len(self.space.m)-len(self.space.infected))*self.factor
        #sir.IM=len(self.space.infected)*self.factor
        self.sir.step(tx,yd) # T is interpolated and the day is the yearday
        #  # s="%d %d %d %d %f %f\n" % (t,mosquitoes,len(self.space.m),len(self.space.infected),self.sir.SM,self.sir.IM)
        s="%d %d %d\n" % (t,(self.sir.SM+self.sir.EM+self.sir.IM)/self.factor,self.sir.IM/self.factor)
        print(s)
        # save the log
        self.log_file.write(s)
        
    def space_step(self,t):
        mosquitoes=self.sir.SM+self.sir.EM+self.sir.IM
        if(mosquitoes>self.sir.NMmin):
            mosquitoes=int(mosquitoes/self.factor)
            diff=mosquitoes-len(self.space.m) 
            if(diff<0):
                self.space.kill(-diff)
            if(diff>0):
                nr=0
                diffI=int(self.sir.IM/self.factor)-len(self.space.infected)
                if(diffI<0):
                    self.space.kill(-diffI)
                if(diffI>0):
                    nr=diffI
                    self.space.addD(nr,infect=True)
                    # print(nr,diffI)
                nr=diff-nr
                self.space.addD(nr,infect=False)
            self.space.step()
            if(len(self.space.m)>100):
                self.sir.SM=(len(self.space.m)-len(self.space.infected))*self.factor
                if(self.highestm<len(self.space.m)):
                    self.m = self.space.get_matrixm()
                    self.highestm=len(self.space.m)
                    print('__________________________________________________',self.highestm)
                if(self.highesti<len(self.space.infected)):
                    self.inf = self.space.get_matrixi()
                    self.highesti=len(self.space.infected)
                    print('**************************************************',self.highesti)
            if(len(self.space.infected) > 1):
                self.sir.IM=len(self.space.infected)*self.factor
            # print(t,':',self.sir.SM,self.sir.LM,self.sir.EM,self.sir.IM)
    def save_matrix(self):
        np.save(path+'/Mosquito-Modeling/SIR/results/matrixm.npy',self.m)
        np.save(path+'/Mosquito-Modeling/SIR/results/matrixi.npy',self.inf)
        
              

""" simulation part """
M=space_simu.mosquitoes(R0n)
simu=SIMU(52.0,M) 
rt=RT.Weather(RT.r1,date(2011,1,1))
# rt=RT.Weather(RT.r1,'20100101')
tx=np.arange(5*365)
""" iterate over one year """
T0=rt.next()
for t in tx:
    if(t%110==0):
        simu.sir.IB+=0.1
    T=(rt.next())*0.1+T0*0.9  # filter it
    T0=T
    simu.time_step(t,T,t%365)
    simu.space_step(t)

simu.save_matrix()
simu.log_file.close()
