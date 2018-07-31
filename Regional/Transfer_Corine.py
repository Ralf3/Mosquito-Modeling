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
gx.read_ascii(path+'/Mosquito-Modeling/Regional/data/clc_resampled.asc')
NPY=gx.get_matp()

#Reclassification:
NPY[NPY == 1]=0.2 #Continuous urban fabric
NPY[NPY == 2]=1 #Discontinuous urban fabric
NPY[NPY == 3]=0.2 #Industrial or commercial units
NPY[NPY == 4]=0.5 #Road and rail networks and associated land
NPY[NPY == 5]=0.8 #Port areas
NPY[NPY == 6]=0.2 #Airports
NPY[NPY == 7]=0 #Mineral extraction sites
NPY[NPY == 8]=0.2 #Dump sites
NPY[NPY == 9]=0.3 #Construction sites
NPY[NPY == 10]=1 #Green urban Areas
NPY[NPY == 11]=1 #Sport and leisure facilities (auch Kleingartenanlagen)
NPY[NPY == 12]=0 #Non-irrigated arable land
NPY[NPY == 13]=0.1 #Permanently irrigated land
NPY[NPY == 14]=0 #Rice fields
NPY[NPY == 15]=0.1 # Vineyards
NPY[NPY == 16]=0.3 # Fruit trees and berry plantations
NPY[NPY == 17]=0.75 # Olive groves (nicht in Deutschland vorhanden)
NPY[NPY == 18]=0.2 #Pastures
NPY[NPY == 19]=0 #Annual crops associated with permanent crops
NPY[NPY == 20]=0.1 #Complex cultivation patterns
NPY[NPY == 21]=0.2 #Land principally occupied by agriculture, with significant areas of natural vegetation
NPY[NPY == 22]=0.1 # Agro-forestry areas
NPY[NPY == 23]=0.9 # Broad-leaved forest
NPY[NPY == 24]=0.1 #Coniferous forest
NPY[NPY == 25]=0.8 # Mixed forest
NPY[NPY == 26]=0 #Natural grasslands
NPY[NPY == 27]=0 # Moors and heathland
NPY[NPY == 28]=0 # Sclerophyllous vegetation
NPY[NPY == 29]=0.6 # Transitional woodland-shrub
NPY[NPY == 30]=0 # Beaches, dunes, sands
NPY[NPY == 31]=0.1 #Bare rocks
NPY[NPY == 32]=0 #Sparsely vegetated areas
NPY[NPY == 33]=0 #Burnt areas
NPY[NPY == 34]=0 #Glaciers and perpetual snow
NPY[NPY == 35]=0 #Inland marshes
NPY[NPY == 36]=0 #Peat bogs
NPY[NPY == 37]=0 #Salt marshes
NPY[NPY == 38]=0 #Salines
NPY[NPY == 39]=0 #Intertidal flats
NPY[NPY == 40]=0 #Water courses
NPY[NPY == 41]=0 #Water bodies
NPY[NPY == 42]=0 #Coastal lagoons
NPY[NPY == 43]=0 #Estuaries
NPY[NPY == 44]=0 #Sea and ocean

gx.write_ascii(path+'/Mosquito-Modeling/Regional/data/clc_resampled1.asc')
