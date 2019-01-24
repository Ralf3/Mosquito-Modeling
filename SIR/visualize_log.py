#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 13:55:35 2018

@author: ralf
"""

""" Visualisation of the simulation results in log.csv """

import pandas as pd
import numpy as np
import pylab as plt

""" read the data in a pandas frame """
path='/datadisk/'
log=pd.read_csv(path+'/Mosquito-Modeling/SIR/results/log.csv', sep=' ')
print(log.describe())

# visualize the infected mosquitoes
infected=log.infected.values
plt.plot(infected)
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('Infected over 4 years')
plt.show()

# visualize the total mosquitoes
total=log.m.values
plt.plot(total)
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('Mosquitoes over 5 years')
plt.show()

""" read teh spactial distributed mosquitoes"""
m=np.load(path+'/Mosquito-Modeling/SIR/results/matrixm.npy')
inf=np.load(path+'/Mosquito-Modeling/SIR/results/matrixi.npy')

plt.figure(figsize=(12,12))
plt.imshow(m)
plt.colorbar()
plt.title('Mosquito distribution')
plt.show()


plt.figure(figsize=(12,12))
plt.imshow(inf)
plt.colorbar()
plt.title('Infected distribution')
plt.show()