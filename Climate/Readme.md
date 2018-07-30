# Climate modeling
## Version 0.1 Dr. Ralf Wieland

The climate model uses data from the DWD and data from the central database for mosquitoes CULBAS, which are stored in Excel files for testing purposes. In accordance with philosophy, the Aedes japonicus compete here against three native mosquitoes. These three species adopt the misoccurrences often used in biological modeling. So, if the Aedes japonicus did not occur, but other mosquitoes do, this place is considered unsuitable. 

The weather data are selected using a feature importance estimation (1981_2010_boost.py) The results can be checked with the programs: 1981_2010_boost_cv.py for the xgboost and 1981_2010_svm.py for the support vector machine.

It should be the Python modules:

* pandas 
* numpy 
* sklearn
* osgeo 
* matplotlib
* pprint
* operator

must be installed.
