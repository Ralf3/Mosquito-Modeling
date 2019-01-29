#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 09:32:29 2018

@author: ralf
"""

""" object oriented modelling for the spatial simulator derived by the 
    simulator.py
    The model implementes the local movement od mosquitoes.
    
    The model interacts with the SIR model supplying the mosquito distribution
    and import the number of living mosquitos, the number of larves, the number
    of infected mosquitoes.
"""

import sys
sys.path.append('/datadisk/samt2/src')
import grid as samt
import numpy as np
import matplotlib.pylab as plt
from scipy.signal import convolve2d
import pickle

class region:
    def __init__(self, nparray):
        self.R=nparray
  
    def get_shape(self):
        return self.R.shape[0], self.R.shape[1]
  
    def get(self,i,j):
        return self.R[i,j]
    
    def show(self):
        plt.imshow(self.R)
        plt.colorbar()
        plt.show()
        
    def save_region(self,filename):
        np.save(filename,self.R)
                
    def load_region(self,filename):
        try:
            self.R=np.load(filename)
        except OSError:
            print('can not open:', filename)
            return False
        return True
        

class mosquito:
    """
    the class mosquito determmines the behavior of one mosquito
    """
    def __init__(self, i1, j1, width1, id, R, energy=100.0, age=0, infect=False):
        self.i=i1          # row of the location in R
        self.j=j1          # column of the location in R
        self.width=width1  # maximum width of jumping 
        self.id=id         # name of the mosquito
        self.infect=infect #  tag if the mosquito is infected 
        self.age=age       # age of the mosquito
        self.energy=energy # energielevel at the begin of the simulation
        self.R=R           # use a defined region
        
        
    def jump(self):
        """ one flight of the mosquito in one day """
        self.age+=1        # I'm one day older now
        height,width=self.R.get_shape()
        i=np.random.randint(-self.width,self.width+1)
        j=np.random.randint(-self.width,self.width+1)
        self.i+=i   # my new row position (y-direction)
        self.j+=j   # my new column position (x-direction)
        if(self.i<0 or self.i>=height or self.j<0 or self.j>=width):
            return False
        self.energy-=(np.abs(i)+np.abs(j))  # energy lost during the flight
        self.energy+=20*self.R.get(self.i,self.j)    # energy gain from R
        if(self.energy>100.0):
            self.energy=100.0
        return True
    
class mosquitoes:
    """ controls all mosqutoes of the simulation """
    def __init__(self,R):
        self.m=[]
        self.infected=[]
        self.steps=0 # count the steps
        self.R=R     # use a defined region
        self.hist2D=self.calc_hist2D()
        self.matrix=np.zeros(self.R.get_shape()) # collect the mosquitoes
        self.energy=np.zeros(self.R.get_shape()) # stores the energy level 
        self.d8_data=np.array([[1,1,1],[1,0,1],[1,1,1]]) # to store the d8 region
        self.distribution = None
        self.migrate=[]  # counts the number of mosquitoes which leave the region
        
    def add(self,mx):
        self.m.append(mx)  # add a single mosquito
        if(mx.infected==True): # is infected so store it
            self.infected.append(mx)
        
    def d8(self,i,j):      # d8 environment
        shape=self.R.get_shape()
        if(i==0 or j==0 or i>=shape[0] or j>=shape[1]):
            return 0
        return np.sum(convolve2d(self.R.R[i-1:i+2,j-1:j+2],self.d8_data,mode='same'))
    
    def calc_hist2D(self):
        """ calculates the spactial hist2D """
        hight, wide = self.R.get_shape()
        hight //= 5
        wide //= 5
        hist2D=np.zeros((hight, wide)) 
        #self.matrix[:,:]=0.0  # reset the mosquito matrix
        #for m in self.m:      # fill it with the mosquitoes
        #    self.matrix[m.i,m.j]+=1
        for i in range(hight):  # fill the 2D historgram
            for j in range(wide):
                hist2D[i,j]=np.sum(self.R.R[5*i:5*i+5,5*j:5*j+5])
        return hist2D
          
    def set_one_mosquito(self,sumOfhist2D,infect=False):
        """ implements the birth process a new mosquito is at the same place like the larve"""
        thresh = np.random.rand()*sumOfhist2D
        sel=0.0
        hight,wide=self.hist2D.shape
        for i in range(hight): 
            for j in range(wide):
                sel+=self.hist2D[i,j]
                if sel>=thresh :
                    self.distribution[i,j]+=1
                    k1=np.random.randint(0,5)
                    k2=np.random.randint(0,5)
                    width=np.random.randint(1,8)
                    m=mosquito(i*5+k1,j*5+k2,width,0,self.R,infect=infect)
                    self.m.append(m)
                    if(infect==True):
                        self.infected.append(m)
                    return
                
    def addD(self,nr,infect=True):
        """ calculates a distribution of nr new mosquitoes 
            the 2D histogram is a matrix with (shape[0]/5,shape[1]/5) cells
            the result is a dist matrix with  (shape[0]/5,shape[1]/5) cells
            containing the part of nr mosquitoes in each cell 
        """
        hight, wide = self.R.get_shape()
        hight //= 5
        wide //= 5
        self.distribution=np.zeros((hight, wide))  # result map
        sumOfhist2D=np.sum(self.hist2D)
        for k in range(nr):
            self.set_one_mosquito(sumOfhist2D,infect)
        return True
    
    def step(self):
        self.steps+=1      # step one day for all stored mosquitoes
        L=[]
        migrate=0
        self.matrix[:,:]=0.0  # reset the mosquito matrix
        for m in self.m:      # fill it with the mosquitoes
            self.matrix[m.i,m.j]+=1
        for m in self.m:
            # test if jump is useful
            if(self.R.get(m.i,m.j)<0.95 or self.d8(m.i,m.j)>80):
                jump_tag=m.jump()
                if(jump_tag==False):
                    migrate+=1
                if(not(jump_tag==False or m.energy<5)):
                    L.append(m) # only if the jump was valid the mosquito survives
                else:
                    try:
                        self.infected.remove(m)
                    except:
                        pass
            else:
                L.append(m)
            #    print(self.steps, m.energy, m.age)
        self.m=L
        self.migrate.append(migrate)
        # print(self.steps,len(self.m))
        
    def kill(self,n):
        """ removes randomly selected mosquitoes """
        ms=np.random.permutation(self.m)
        for k in range(n):
            self.m.remove(ms[k])
            if ms[k] in self.infected:
                self.infected.remove(ms[k])
        return True
        
    def show(self):
        """ show the mosquitoes as points """
        self.matrix[:,:]=0.0  # reset the mosquito matrix
        for m in self.m:      # fill it with the mosquitoes
            self.matrix[m.i,m.j]+=1
        plt.imshow(self.matrix)
        plt.colorbar()
        plt.show()
        
    def show_energy(self):
        """ show the energy level of the mosquitoes """
        self.energy[:,:]=0.0
        for m in self.m:
            self.energy[m.i,m.j]+=m.energy
        plt.imshow(self.energy)
        plt.colorbar()
        plt.show()
        
    def get_number(self):
        """ retruns the number of mosquitoes wich are alive and in R """
        return len(self.m)
    
    def save_mosquitoes(self,filename):
        """ save the list of mosquitoes """
        f=open(filename,'wb')
        pickle.dump(self.m,f)
        f.close()
        
    def load_mosquitoes(self,filename):
        """ reads the mosquitoes from disk """
        try:
            f=open(filename,'rb')
        except OSError:
            print('can not open:', filename)
            return False
        self.m=pickle.load(f)
        f.close()
        return True
    
    def get_matrixm(self):
        matrix=np.zeros(self.R.get_shape())  # reset the mosquito matrix
        for m in self.m:      # fill it with the mosquitoes
            matrix[m.i,m.j]+=1.0
        return matrix
    
    def get_matrixi(self):
        matrix=np.zeros(self.R.get_shape())  # reset the mosquito matrix
        for m in self.infected:      # fill it with the mosquitoes
            matrix[m.i,m.j]+=1.0
        return matrix
       
        
        
    
