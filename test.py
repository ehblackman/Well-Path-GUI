import well_profile as wp
import pandas as pd

path = 'test well data'
collar = 'Collar GUI.csv'
survey = 'Survey GUI.csv'

collar = pd.read_csv(f'{path}/{collar}')
for key in collar.keys():
    if 'latitude' in key.lower():
        lat = collar[key]
    elif 'longitude' in key.lower():
        long = collar[key]

well = wp.load(f'{path}/{survey}',   # define target depth (md) in m or ft
                   units='metric',  # (optional) define system of units 'metric' for meters or 'english' for feet
                   set_start={'north': lat[0], 'east': long[0], 'depth': 0})  # (optional) set the location of initial point

well.plot(names=['Test']).show()

