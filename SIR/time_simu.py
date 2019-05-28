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
        self.nuB = 0.7        # portion of dead bird
        # self.nuB = 0.2        # test number from Ralf

        """ mosquito part of parameter 
            this should be paramters for the modelling interface """
        self.KM = 300000  #7500#30.0#100.0   # carrying capccity of mosquitoes
                          # from Rubel estimated as 3,300,000 for Cx.pipiens comple
        self.scale = 1    # scale factor between KM and real word of deseases (new!)
        self.NMmin = 100.0  # minimum number of mosquitoes
        # self.mE  = 0.02  # mortality of an egg
        
        """ bird parameter """
        self.KB = 10000 # carrying capacity of the bird
                        # originally calculated as total number
                        # of birds in a disease free population, 
                        # 110,000 for American crow
                        
        """ transfer from bird to mosquito and vise versa """
        #self.pM = 1.0   # probable transmition of des. from mosquito to the bird
        #self.pM = 1.2   # assumption from RALF
        self.pM = 1.0    # transmition rate from infectious mosquito to the bird
        #self.pB = 0.125  # transmission rate from bird to mosquito
        #self.pB = 0.2  # assumption from RALF
        self.pB = 0.5
    """ mosquito part of parameter """
    
    def biting_rate(self,T):
        """ dieser Parameter ist nur noch für die Infektionen wichtig 
        (nicht wegen jedem Stich werden Eier abgelegt)
        T: temperature in grd C 
        """
        return 0.344/(1+1.231*np.exp(-0.184*(T-12))) # it should be much lower for Aedes japonicus 
                                                     # regarding to BIRD-BITES!; its 
                                                     # gonotrophic cycle, which this equation describes,
                                                     # however, should not be so different 
    def proportion_bited_birds(self,T):
        return (0.344/(1+1.231*np.exp(-0.184*(T-12))))
        
    
    def bL(self,T):
        """ birth rate of larve T: temperature in grd C """
        return 2.325 * self.biting_rate(T)  # it should be much more complicated! Die Anzahl
                                            # der Nachkommen/Weibchen ist temperaturabhängig: umso kälter,
                                            # desto größer das Weibchen und umso mehr Nachkommen; 
                                            # auch die Entwicklungszeit (Temp-abhängig) ist wichtig!
    def bM(self,T):
        """ birth rate of mosquito """
        return self.bL(T)*0.1 #aus dem Rubel-Modell
    
    def mL(self,T):
        """ mortality of the larve T: temperature in grd C """
        return 0.0025*T**2-0.094*T+1.0257         # from Rubels Usutu model/ West Nil model
        # return 0.3018*T**2-10.9962*T+116.1783   # after Reuss et al, 2018
        # return 0.0024*T**2-0.09*T+1.0257        # new assumption
    
    def mM(self,T):
        """ mortality rate of the mosquito T: temperature in grd C """
        
        return 0.1*self.mL(T) #aendern!!!???
    
    def betaM(self,T):
        """ transmission rate """
        #return self.biting_rate(T)*self.pM
        return self.proportion_bited_birds(T)*self.pM
    
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
        """ fraction of active, not diapausing mosquitoes """
        #return 1.0-1.0/(1.0+10775.7*np.exp(1.559*(self.daylength(dayOfYear)-18.177))) #Kurve verbreitert
        return 1.0-1.0/(1.0+1775.7*np.exp(1.559*(self.daylength(dayOfYear)-18.177))) #Rubel
    
    def gammaM(self,T):
        """ rate infected-infectious, T: temp in grd C"""
        if(T<=10):
            return 0.0
        # return 0.0093*T-0.1352
        return 0.0093*T-0.093
    
    
    
    """ the bird part of parameters """
    
    def bB(self,dayOfYear):
        """ Bird birth (bB) as function of the year
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
        #return self.biting_rate(T)*self.pB
        return self.proportion_bited_birds(T)*self.pB
    

    """ simulation part """
    
    def set_init_conditions(self,lm=10000.0,sm=25000.0,im=0.0,sb=9500.0,ib=0.0):
        """ init the simulation by setting the starting parameters """
        if(sm<self.KM):
            self.SM = sm     # start mosquitoes
        else:
            self.SM=self.KM/2
        if(lm<self.KM):
            self.LM = lm     # larve
        else:
            self.LM=self.KM/2
        self.EM = 0.0    # expected mosquitos
        self.IM = im     # infected mosquitos
        if(sb<self.KB):
            self.SB = sb     # start bird
        else:
            self.SB=self.KB/2
        self.EB = 0.0    # expected bird
        self.IB = ib     # infected bird
        self.RB = 0.0    # recovered bird
        self.DB = 0.0    # dead bird
        # self.model=[self.LM,self.SM,self.EM,self.IM,self.SB,self.EB,self.IB,self.RB,self.DB]

    def lambdaMB(self,T, dayOfYear):
        """ transfer mosquitoes to birds """
        return self.deltaM(dayOfYear) * self.betaM(T) * self.pM * self.KM/self.KB * self.IM/self.KM # 
        #return self.deltaM(dayOfYear) * self.betaM(T) * 30 * self.IM/self.KM

    def lambdaBM(self,T, dayOfYear):
        """ transfer birds to mosquitoes """
        return self.deltaM(dayOfYear) * self.betaB(T) * self.IB/self.KB

        
    def  step(self,T,dayOfYear):
        """ one time step with a simple euler method dh=1
            T= temp in grd C, dayOfYear
        """
        SM = self.SM     # save the old state for reconstraction
        EM = self.EM
        IM = self.IM
        LM = self.LM
        #EG = self.EG
        # birds
        SB = self.SB
        EB = self.EB
        IB = self.IB
        RB = self.RB
        dayOfYear+=1  # from 1,...
        
        #lambdaB = self.deltaM(dayOfYear)*self.pB*self.IB/self.KB # transfer mosquito to bird
        #lambdaM = self.deltaM(dayOfYear)*self.pM*self.IM/self.KM # 
        
        """Bird Population Loop"""
        bB = self.bB(dayOfYear)
        NB = SB+EB+IB+RB 
        self.SB += (bB-(bB-self.mB)*NB/self.KB) * NB- self.lambdaMB(T,dayOfYear) * SB -self.mB*SB
        self.EB += self.lambdaMB(T,dayOfYear)*SB - self.gammaB*EB - self.mB*EB
        self.IB += self.gammaB*EB - self.alphaB*IB - self.mB*IB #ok
        self.RB += (1-self.nuB)*self.alphaB*IB-self.mB*RB #ok
        self.DB += self.nuB*self.alphaB*self.IB 
        # print(self.SB,self.EB,self.IB,self.RB,self.DB)
         
        """mosquito pop"""
        NM = SM+EM+IM # sum of all mosquitoes in all states
        self.LM += (self.bL(T)*self.deltaM(dayOfYear)*NM -self.mL(T)*LM)*(1-LM/self.KM) - self.bM(T)*self.LM
        self.SM += -self.lambdaBM(T,dayOfYear) * SM + self.bM(T) *self.LM -self.mM(T) * SM
        self.EM += self.lambdaBM(T,dayOfYear)*SM - self.gammaM(T)*EM - self.mM(T) *EM
        self.IM += self.gammaM(T) * self.EM - self.mM(T) * IM 
        # print(T,dayOfYear,self.LM,self.SM,self.EM,self.IM)
        
        # check of valid 
        if self.SM<0 :
            self.SM=100
        NM = self.SM+self.EM+self.IM
        if NM<self.NMmin : 
            self.SM = 100
        if(self.EM<0):
            self.EM = 0.1
        if(self.IM<0):
            self.IM = 0.1
        if(self.LM<0):
            self.LM = 0.1
            
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
    
    """bited birds"""
    proportion_bited_birds=sir.proportion_bited_birds(T)
    plt.plot(T,proportion_bited_birds)
    plt.grid()
    plt.xlabel('Temperature (°C)')
    plt.ylabel('bird biting rate (1/day)')
    plt.title('Specific bird biting rate against Temperature')
    plt.show()
    
    """ Mosquito fecundity """
    ###entfernt
    
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
    
    """ transmission rate (betaB) von Vogel zu Mücke """
    T=np.linspace(-5.0,45.0,100)
    betaB=sir.betaB(T)
    plt.plot(T,betaB)
    plt.grid()
    plt.xlabel('Temperature (°C)')
    plt.ylabel('betaB (1/day)')
    plt.title('transmission rate (betaB: Vogel zu Mücke)\nagainst temperature')
    plt.show()
    
    """ Birth birds """
    t=np.linspace(1,365,365)  # days
    bB=[]
    for tx in t:
        bB.append(sir.bB(tx))
    plt.plot(t,bB)
    plt.grid()
    plt.xlabel('time in days')
    plt.ylabel('bB')
    plt.title('Bird birth rate')
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
    return sir

"""
sir=show_tests()                                             
sir.set_init_conditions(sm=10000,lm=50000,sb=9800,ib=0)
"""
