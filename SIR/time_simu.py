#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 09:39:41 2018

@author: ralf
"""

""" The time simulator is derived by the SIR.py. It implements the 
    developmewnt in time and the interaction with the birds. 
    It uses the intial number of mosquitoes (mapping it to a number between
    1..100). After each time step the number of mosquitoes is corrected 
    according to the mosquitoes which came in the region or which leaved
    the region. 
    The time simulator supplies the number of living mosquitoes, and the
    number of infected mosquitoes.
"""

""" SIR Model according to Franz Rubel Vienna for Mosquotoes """

import numpy as np
from scipy.stats import gamma
   
class SIR:
    def __init__(self,lat):
        self.lat = lat    # latitdude of the region

        """ the bird part of parameters """
        # for Usustu-virus
#        self.mB = 0.0012     # mortality rate of bird
#        self.alphaB = 0.182  # recovery rate of bird
#        self.gammaB = 0.667  # incubition rate of bird
#        self.nuB = 0.3       # portion of dead bird
        #for West-Nile-virus
        self.mB = 0.00034     # mortality rate of bird
        self.alphaB =0.4      # recovery rate of bird
        self.gammaB = 1.0     # incubition rate of bird
        self.nuB = 0.2        # portion of dead bird

        """ mosquito part of parameter 
            this should be paramters for the modelling interface """
        self.KM = 100.0   # carrying capccity of mosquitoes
        self.scale = 20   # scale factor between KM and real word of deseases
        self.NMmin = 1.0  # minimum number of mosquitoes
        # self.mE  = 0.02  # mortality of an egg
        """ bird parameter """
        self.KB = 5.0   # carrying capacity of the bird
        """ transfer from bird to mosquito and vise versa """
        self.pM = 1.0        # prob. transmition of des. from mosquito to the bird
        self.pB = 0.125      # prop. from bird to mosquito
        
    """ mosquito part of parameter """
    
    def biting_rate(self,T):
        """ T: temperature in grd C """
        return 0.344/(1+1.231*np.exp(-0.184*(T-20)))
    
    def bL(self,T):
        """ birth rate of larve T: temperature in grd C """
        return 2.325 * self.biting_rate(T)
    
    def bM(self,T):
        """ birth rate of mosquito """
        return self.bL(T)*0.1
    
    def mL(self,T):
        """ mortality of the larve T: temperature in grd C """
        return 0.0025*T**2-0.094*T+1.0257
    
    def mM(self,T):
        """ mortality rate of the mosquito T: temperature in grd C """
        
        return 0.1*self.mL(T)
    
    def betaM(self,T):
        """ transmission rate """
        return self.biting_rate(T)*self.pM
 
    def daylength(self, dayOfYear):
        """
        Computes the length of the day the time between sunrise and
        sunset, given the day of the year and latitude of the location.
        Function uses the Brock model for the computations.
        For more information see, for example,
        Forsythe et al., A model comparison for daylength as a
        function of latitude and day of year, Ecological Modelling,
        Parameters
        ----------
        dayOfYear : int
        The day of the year. 1 corresponds to 1st of January
        and 365 to 31st December (on a non-leap year).
        lat : float
        Latitude of the location in degrees. Positive values
        for north and negative for south.
        Returns
        -------
        d : float
        Daylength in hours.
        """
        latInRad = np.deg2rad(self.lat)
        declinationOfEarth = 23.45*np.sin(np.deg2rad(360.0*(283.0+dayOfYear)/365.0))
        if -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) <= -1.0:
            return 24.0
        elif -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) >= 1.0:
            return 0.0
        else:
            hourAngle = np.rad2deg(np.arccos(-np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth))))
        return 2.0*hourAngle/15.0
    
    def deltaM(self,dayOfYear):
        """ fraction of active mosquitoes diapausing mosquitoes """
        # return 1.0-1.0/(1.0+1775.7*np.exp(1.559*(self.daylength(dayOfYear)-18.177)))
        return 1.0-1.0/(1.0+1775.7*np.exp(1.559*(self.daylength(dayOfYear)-18.177)))
    
    def gammaM(self,T):
        """ rate infected-infectious, T: temp in grd C"""
        if(T<=15):
            return 0.0
        return 0.0093*T-0.1352
    
    """ the bird part of parameters """
    
    def bB(self,dayOfYear):
        """ betaB as function of the year
            bB was adapted to the gamma distribution to make it easier to
            apdat it to new data
        """
        x = (dayOfYear-80)/5.5   # transformed Julian calender day
        if(x<=0):
            return 0.0
        # alpha = 8.157894736842106
        alpha = 16.0
        rv = gamma(alpha)
        # return 0.025*rv.pdf(x)
        return 0.065*rv.pdf(x)
    
    def betaB(self,T):
        """ transmission rate"""
        return self.biting_rate(T)*self.pB
    
    def eggs(self,T):
        """ describes the number of eggs laid per clutch
            this was normalized to a rate for self.EG
        """
        max_eggs=214.61702127659566
        if(T<10.0):
            return 0.0
        elif(T>=28.5):
            return 16.76542553191486/max_eggs
        return (-0.00245*T**2 + 0.04406*T + 0.81310) / 0.0047 / max_eggs
     
    def mE(self,T):
        """mortality rate of mosquito eggs (per 4 day)"""
        return (0.9*(1-( 1 / (1 + np.exp(-0.26157921*(T-0.46877381)))))+0.1) / 5.0
    
    """ simulation part """
    
    def set_init_conditions(self,sm=1.0,lm=1.0,im=0.01,sb=0.5,ib=0.05):
        """ init the simulation by setting the starting parameters """
        self.SM = sm     # start mosquitoes
        self.EG = 0.1    # eggs 
        self.LM = lm     # larve 
        self.EM = 0.0    # expected mosquitos
        self.IM = im     # infected mosquitos
        self.SB = sb     # start bird
        self.EB = 0.0    # expected bird
        self.IB = ib     # infected bird
        self.RB = 0.0    # recovered bird
        self.DB = 0.0    # dead bird
        self.model=[self.LM,self.SM,self.EM,self.IM,self.SB,self.EB,self.IB,self.RB,self.DB]
        
    def  step(self,T,dayOfYear):
        """ one time step with a simple euler method dh=1
            T= temp in grd C, dayOfYear
        """
        SM = self.SM     # save the old state for reconstraction
        EM = self.EM
        IM = self.IM
        LM = self.LM
        EG = self.EG
        # birds
        SB = self.SB
        EB = self.EB
        IB = self.IB
        RB = self.RB
        dayOfYear+=1  # from 1,...
        
        #lambdaB = self.deltaM(dayOfYear)*self.pB*self.IB/self.KB # transfer mosquito to bird
        #lambdaM = self.deltaM(dayOfYear)*self.pM*self.IM/self.KM # 
        # Bird Population Loop
        bB = self.bB(dayOfYear)
        NB = SB+EB+IB+RB # +self.DB
        self.SB += (bB-(bB-self.mB)*NB/self.KB)*NB-self.deltaM(dayOfYear)*self.betaM(T)*IM*SB/self.KB-self.mB*SB
        self.EB += self.deltaM(dayOfYear)*self.betaM(T)*IM*self.SB/self.KB-self.gammaB*EB-self.mB*EB
        self.IB += self.gammaB*self.EB-self.alphaB*IB-self.mB*IB
        self.RB += (1-self.nuB)*self.alphaB*self.IB-self.mB*RB
        self.DB += self.nuB*self.alphaB*self.IB # +self.mB*(self.SB+self.EB+self.IB+self.RB)
        # print(self.SB,self.EB,self.IB,self.RB,self.DB)
        # mosquito pop
        NM = SM+EM+IM+LM # sum of all mosquitoes in all states
        # self.EG += self.eggs(T)*self.deltaM(dayOfYear)*NM*(1-EG/self.KM)-self.mE(T)*self.EG-(self.bL(T)*self.deltaM(dayOfYear)*self.EG)
        self.LM += (self.bL(T)*self.deltaM(dayOfYear)*NM-self.mL(T)*LM)*(1-LM/self.KM)-self.bM(T)*LM
        self.SM += self.bM(T)*self.LM-self.scale*self.deltaM(dayOfYear)*self.betaB(T)*SM*IB/self.KB-self.mM(T)*SM
        self.EM += self.scale*self.deltaM(dayOfYear)*self.betaB(T)*self.SM*IB/self.KB-self.scale*self.gammaM(T)*EM-self.mM(T)*EM
        self.IM += self.scale*self.gammaM(T)*self.EM-self.mM(T)*IM
        print(self.LM,self.SM,self.EM,self.IM)
        # check of valid 
        if self.SM<0 :
            self.SM=0.01
        NM = self.SM+self.EM+self.IM+self.LM
        if NM<self.NMmin : 
            self.SM = SM 
            self.EM = EM
            self.IM1 =IM
            
import pylab as plt       
def show_tests():
    lat=52.0
    sir=SIR(lat)
    """ biting_rate """
    T=np.linspace(-5.0,45.0,100)
    biting_rate=sir.biting_rate(T)
    plt.plot(T,biting_rate)
    plt.grid()
    plt.xlabel('Temperature (°C)')
    plt.ylabel('biting rate (1/day)')
    plt.title('Biting rate against Temperature')
    plt.show()
    """ Mosquito fecundity """
    """ gammaM """
    gammaM=[]
    for TX in T:
        gammaM.append(sir.gammaM(TX))
    plt.plot(T,gammaM)
    plt.grid()
    plt.xlabel('Temperature (°C)')
    plt.ylabel('gammaM')
    plt.title('rate infected-infectious, T: temp in grd C')
    plt.show()
    """ ML """
    mL=[]
    for TX in T:
        mL.append(sir.mL(TX))
    plt.plot(T,mL)
    plt.grid()
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Larval mortality, mL (1/d)')
    plt.title('mortality of the larve T: temperature in grd C')
    plt.show()
    """ deltaM """
    t=np.linspace(1,365,365)  # days
    deltaM=[]
    for tx in t:
        deltaM.append(sir.deltaM(tx))
    plt.plot(t,deltaM)
    plt.grid()
    plt.xlabel('time in days')
    plt.ylabel('deltaM')
    plt.title('fraction of active, not diapausing mosquitoes')
    plt.show()
    bB=[]
    for tx in t:
        bB.append(sir.bB(tx))
    plt.plot(t,bB)
    plt.grid()
    plt.xlabel('time in days')
    plt.ylabel('dB')
    plt.title('transmission rate (beta) as function of the year')
    plt.show()
    """ daylength """
    daylength=[]
    for tx in t:
        daylength.append(sir.daylength(tx))
    plt.plot(t,daylength)
    plt.grid()
    plt.xlabel('time in days')
    plt.ylabel('daylength')
    plt.title('daylength as function of the year')
    plt.show()
#    eggs1=[]
#    for TX in T:
#        eggs1.append(sir.eggs(TX))
#    plt.plot(T,eggs1)
#    plt.grid()
#    plt.xlabel('Temperature (°C)')
#    plt.ylabel('Mean number of eggs per female')
#    plt.title('Fecundity')
#    plt.show()
#    eggs2=[]  
#    for TX in T:
#        eggs2.append(sir.mE(TX))
#    plt.plot(T,eggs2)
#    plt.grid()
#    plt.xlabel('Temperature (°C)')
#    plt.ylabel('Mortality rate of eggs')
#    plt.title('Mortality')
#    plt.show()
 
    return True


show_tests()                                             