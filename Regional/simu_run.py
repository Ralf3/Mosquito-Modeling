#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Tue Sep 19 14:23:57 2017

@author: ralf
"""

""" Fuzzy Modelle Antje Kerkow:
    Landscape, Wind, Climate
"""


import sys
import os
import numpy as np
sys.path.append(os.environ["SAMT2MASTER"]+'/fuzzy/src')
import Pyfuzzy as fuzz
sys.path.append(os.environ["SAMT2MASTER"]+'/src')
import grid as samt2 
import time 

# load fuzzy model
# path='/home/kerkow/Aufbau_Fuzzy/Modell/Version3/'
path='/datadisk/pya/culifo_June_2018/culifo_regional/'
f=fuzz.read_model(path+'LandscapeMosquitoes3.fis',)


# load the ASCII or HDF-files
landscape=samt2.grid()
landscape.read_ascii(path+'Landscape_Version2_MW_7.asc')
wind=samt2.grid()
wind.read_hdf(path+'wind100m.hdf','wind100m')
climate=samt2.grid()
climate.read_ascii(path+'ClimateModelOutputs_callibrated/ClimateSuitability_1981_2010_100m.asc')
#climate.read_ascii(path+'ClimateModelOutputs_callibrated/ClimateSuitability_2051_2080_100m.asc')
#
# start the simulation
t0=time.time()
modell=f.grid_calc3(landscape,wind,climate)
print( 'calc time:',time.time()-t0)
# save the model
#modell.write_ascii(path+'FuzzyResult_Version3_1981_2010.asc')
#modell.write_ascii(path+'FuzzyResult_Version3_2051_2080.asc')
modell.write_ascii(path+'FuzzyResult_Version3_1981.asc')
# show it
modell.show()



