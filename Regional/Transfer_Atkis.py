#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 10:32:57 2018

@author: ralf
"""

import sys
import os
sys.path.append(os.environ['SAMT2MASTER']+"/src")
import grid as samt2
import numpy as np

gx=samt2.grid()

path='/datadisk/'
gx.read_ascii(path+'/Mosquito-Modeling/Regional/data/Atkis.asc')
NPY=gx.get_matp()

#Reclassification:
NPY[NPY == 65535]=-999   #Nodata Value
NPY[NPY == 2213]=1   #Friedhöfe
NPY[NPY == 2122]=0.2 #Deponien
NPY[NPY == 2132]=1   #Gärtnereien
NPY[NPY == 2225]=1   #Zoos
NPY[NPY == 4103]=1   #Gartenland

gx.write_ascii(path+'/Mosquito-Modeling/Regional/data/Atkis1.asc')
