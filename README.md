# Well-Path-GUI

Well bore GUI

A WELL (aka BOREHOLE) always has a unique well name (UWI)

Collar

1.	Each WELL has a COLLAR. This records the XYZ coordinates of the top of the well (Earth’s Surface).
2.	This is stored as longitude, latitude, Elevation above sea level (metres). 
3.	The coordinate system is NAD83 UTM zone 11. 

Survey 

1.	Each WELL has SURVEY DATA which records: AZIMUTH (degrees) and DIP (degrees) at a given DEPTH (metres).
2.	This describes the direction of the well path through the Earth’s crust. 
3.	A VERTICAL well is defined as AZIMUTH = 0, INCLINATION = 0. 

A WELL may contain a SAMPLE:

1.	A sample has 2 DEPTH INVERVALS: this describes the distance between 2 depths along the WELL PATH which were sampled. E.g interval top = 1000m, interaval bottom = 1010m. So the sample was collected between 1000 and 1010m of the WELL PATH. Note this DOES NOT MEAN 1000-1010m TRUE VERTICAL DEPTH (TVD) or elevation. 
2.	A sample also contains geochemical data such as the % of CO2 in the sampled gas. 
