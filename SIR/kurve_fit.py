#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 17:15:11 2018

@author: ralf

This is only a simple file to adapt a gamma distribution.
It is only for me to make the code easier to adapt to new data
"""

import numpy as np
import pylab as plt
import scipy.stats as stats   
from scipy.stats import gamma


# generate a sample
gammaP = np.zeros(1000)
gammaC = np.zeros(1000)
g=4.789473684210526
x = np.linspace(gamma.ppf(0.0001,g),gamma.ppf(0.99,g),1000)
# rv=gamma(fit_alpha)
rv = gamma(g)
for i in range(gammaP.size):
    gammaP[i] = rv.pdf(x[i])
    gammaC[i] = rv.cdf(x[i])
plt.plot(x,gammaP) 
plt.plot(x,gammaC) 
plt.grid()  
plt.show()

for i in np.linspace(5,10,20):
    print(i, ' : ',gamma.ppf(0.001,i),gamma.ppf(0.5,i),gamma.ppf(0.99,i))
    
def bB(dayOfYear):
        """ betaB as function of the year """
        x = (dayOfYear-80)/5.5   # transformed Julian calender day
        if(x<=0):
            return 0.0
        alpha = 8.157894736842106
        rv = gamma(alpha)
        return 0.025*rv.pdf(x)

T=range(80,180)
D=[]
for t in T:
    D.append(bB(t))

plt.plot(T,D) 
plt.grid()
plt.show()
