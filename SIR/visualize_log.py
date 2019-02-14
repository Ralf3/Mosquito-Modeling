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
import sys

""" read the data in a pandas frame """
#path='/datadisk/'
#log=pd.read_csv(path+'results/log.csv', sep=' ')
path='/datadisk/Mosquito-Modeling/SIR/'
log=pd.read_csv(path+'results/log.csv', sep=' ')
print(log.describe())

# visualize the LM
plt.figure(figsize = (9,5))
plt.plot(log.LM.values, label='LM')
plt.plot(log.SM.values, label='SM')
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('LM/SM over 5 years')
plt.show()

"""
# visualize the total mosquitoes
total=log.SM.values
plt.figure(figsize = (9,5))
plt.plot(total)
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('SM over 5 years')
plt.show()
"""

# visualize the exposed mosquitoes
EM=log.EM.values
plt.figure(figsize = (9,5))
plt.plot(EM)
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('Exposed (EM) over 5 years')
plt.show()

# visualize the infected mosquitoes
IM=log.IM.values
plt.figure(figsize = (9,5))
plt.plot(IM, color="r")
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('Infectious (IM) over 5 years')
plt.show()


#visualize the susceptible birds (SB)
SB=log.SB.values
plt.figure(figsize = (9,5))
plt.plot(SB)
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('Susceptible birds (SB) over 5 years')
plt.show()

#visualize the exposed birds (EB)
EB=log.EB.values
plt.figure(figsize = (9,5))
plt.plot(EB)
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('Exposed birds (EB) over 5 years')
plt.show()

#visualize the infectious birds (IB)
IB=log.IB.values
plt.figure(figsize = (9,5))
plt.plot(IB, color="r")
plt.ylabel('nr')
plt.xlabel('day')
plt.grid()
plt.title('Infectious birds (IB) over 5 years')
plt.show()


""" read the spactial distributed mosquitoes"""
m=np.load(path+'results/matrixm.npy')
inf=np.load(path+'results/matrixi.npy')

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
