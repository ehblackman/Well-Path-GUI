# Well-Path-GUI

Well bore GUI


This package creates a file browser GUI in which you can select and import a well database in the form of multiple csv files. These csv files are then used to create pandas dataframes. These dataframes are manipulated, cleaned and standardised.

Once the dataframes are prepped, several calculations take place by a number of functions. The primary purpose is to provide downwell samples such as DST fluid analyses with x, y and z data. This is done for all well paths, regardless of trajectory.

This enables samples to be plotted in 3D space, without needing to plot the well trajectory in which the sample was derived. The same functions are also applied to geological formation tops.





A WELL (aka BOREHOLE) always has a unique well name (UWI)

1.	Each WELL has a COLLAR. This records the XYZ coordinates of the top of the well (Earth’s Surface).
2.	This is stored as longitude, latitude, Elevation above sea level (metres). 
3.	The coordinate system is NAD83 UTM zone 11. 

1.	Each WELL has a SURVEY which records: AZIMUTH (degrees) and INCLINATION (degrees) at a given DEPTH (metres).
2.	This describes the direction of the well path through the Earth’s crust. 
3.	A VERTICAL well is defined as AZIMUTH = 0, INCLINATION = 0. 

A WELL may contain a SAMPLE:
1.	A sample has 2 DEPTH INVERVALS: this describes the distance between 2 depths along the WELL PATH which were sampled. E.g interval top = 1000m, interval bottom = 1010m. So the sample was collected between 1000 and 1010m of the WELL PATH. Note this is measured depth along the well path and DOES NOT MEAN 1000-1010m TRUE VERTICAL DEPTH (TVD) or elevation. 
2.	A sample also contains geochemical data. For example % of CO2 in the sampled gas.
3.	A sample depth is the MIDPOINT between the top and bottom intervals.
