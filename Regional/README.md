# Regional modeling usong fuzzy modeling

The idea here is to build a fuzzy model based on SAMT2 which contains three inputs: 

*	landscape
*	climate as the result of climate modeling
*	a wind map from DWD

The landscape was generated using corine landcover and Atkis data. The transfer tables which
change the coded landuse types to suitablitlity indices are given in:

*      Transfer_Corine.py
*      Transfer_Atkis.py

The input data are compressed in data:

*   Atkis.asc.tgz
*   clc_resampled.asc.tgz

The landscape was filtered to remove hard borders in the map. A moving window radius of
700m was selected and a simple program was implemented to appy the moving window to a 
grid. 

*	moving_window.py


The used data sets are too big to store int in GitHub so the user is requested to ask for the data personally. 

