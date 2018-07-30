# Mosquito-Modeling
## Mosquito modeling based on machine learning, fuzzy modeling and dynamic propagation

The modelling part focuses on modelling the spread of the invasive mosquito species Aedes japonicus, which is a potential carrier of diseases. The model concept is easily transferable to other mosquito species (insect species). The modelling approach starts with modelling the habitat suitability of Aedes japonicus under the influence of climate. In the second step, the regional characteristics of (microhabitats) are added using fuzzy modeling. The third step is to model the regional spread and transmission of diseases on the basis of an SIR model in which the Aedes japonicus appears as a vector and infects birds or transmits the virus from birds.

From the point of view of information technology, all three steps take place on a different basis. The climate model uses as data source a database of sites of mosquitoes including the Aedes japonicus. These data and the data of the German Weather Service (DWD) are used to model the climate dependency of the Aedes japonicus. A support vector machine is used, which generates quite robust-like models even with few available data.

The regional habitat suitability studies the influence of regional structures, such as urban areas, allotments etc. together with the wind data of the DWD and the result of the climate model from step one, on the regional occurrence of the Aedes japonicus.

In the third part, the spread of a disease for which Aedes japonicus serves as a vector is modeled. Here the dynamics of the transmission of Aedes japonicus' disease to birds (or of birds to Aedes japonicus) is an essential part of the model. The model comprises a dynamic part and a spatial part. The spatial part models the movement of the mosquitoes in the region, while the dynamic part implements the individual time steps - this is comparable to the solution of a partial differential equation.

