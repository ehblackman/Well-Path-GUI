from OLD.classes import Collar, Well, Survey, Sample
import well_profile as wp
import pandas as pd


# File import
path = 'test well data'
collar_csv = 'Collar GUI.csv'
survey_csv = 'Survey GUI.csv'
sample_csv = 'Sample GUI.csv'
geology_csv = 'Geology GUI.csv'

def import_collar(path, collar_csv, survey_data):
    # Load collar from CSV files to pandas dataframes
    collar_data = pd.read_csv(f'{path}/{collar_csv}')

    # Preprocessing
    change_alternative_to_uwi(collar_data)
    # Call the function to change column names
    #This means we can use UWI as the well name across dataframes
    # Convert the "UWI" column to string data type in collar_data
    collar_data['UWI'] = collar_data['UWI'].astype(str)

    collar_data['well'] = collar_data['UWI'].apply(lambda u: load_well(collar_data, survey_data, u))
    
    return collar_data

def load_well(collar_data, survey_data, uwi):
    collar = collar_data[collar_data['UWI']==uwi]
    well_data = survey_data[survey_data['UWI']==uwi]
    north = float(list(collar['Surf-Hole Northing (NAD83)'])[0])
    east = float(list(collar['Surf-Hole Easting (NAD83)'])[0])
    well = wp.load(well_data, set_start={'north': north, 'east': east, 'depth': 0})   
    return well
    
def import_survey(path, survey_csv):
    # Load data
    survey_data = pd.read_csv(f'{path}/{survey_csv}')

    # Preprocessing
    change_alternative_to_uwi(survey_data)
    # Convert the "UWI" column to string data type in survey_data
    survey_data['UWI'] = survey_data['UWI'].astype(str)

    survey_data = survey_data.rename(columns={'Azimuth Angle': 'azi'})
    survey_data = survey_data.rename(columns={'Inclination': 'inclination'})
    survey_data = survey_data.rename(columns={'Measured Depth': 'md'})

    return survey_data

def import_sample(path, sample_csv, collar_data):
    # Load data
    sample_data = pd.read_csv(f'{path}/{sample_csv}')
    
    # Preprocessing
    change_alternative_to_uwi(sample_data)
    # Convert the "UWI" column to string data type in sample_data
    sample_data['UWI'] = sample_data['UWI'].astype(str)

    # Processing
    # Calculate and add a new column 'MidpointDepth' to sample_data
    sample_data['sample_midpoint_depth'] = (sample_data['Interval Base(m)'] + sample_data['Interval Top(m)']) / 2
    # Delete rows with missing 'Interval Top(m)' or 'Interval Base(m)' data in sample_data
    sample_data = sample_data.dropna(subset=['Interval Top(m)', 'Interval Base(m)'])

    # Get tvd
    sample_data = get_point_info(collar_data, sample_data, col_name='sample_midpoint_depth')

    # Add ground elevation to sample data
    sample_data['Ground Elevation'] = sample_data['UWI'].apply(lambda u: get_col_UWI(collar_data, u, 'Ground Elevation (m)'))
    sample_data['Sample Depth Below Sea Level'] = sample_data['Ground Elevation'] - sample_data['TVD']

    return sample_data

def import_geology(path, geology_csv, collar_data):
    # Load data
    geology_data = pd.read_csv(f'{path}/{geology_csv}', skiprows=15)
    change_alternative_to_uwi(geology_data)
    geology_data['UWI'] = geology_data['UWI'].astype(str)


    # Get Northing / Easting (see get point further down)
    geology_data = get_point_info(collar_data, geology_data, depth_type_to_query='md', col_name='TVD')

    # Add ground elevation to sample data
    geology_data['Ground Elevation'] = geology_data['UWI'].apply(lambda u: get_col_UWI(collar_data, u, 'Ground Elevation (m)'))
    geology_data['Sample Depth Below Sea Level'] = geology_data['Ground Elevation'] - geology_data['TVD']

    return geology_data
    
def get_col_UWI(df, uwi, col):
    return list(df.loc[df['UWI']==uwi][col])[0]

def change_alternative_to_uwi(dataframe):
    '''# Function to change alternative column names to "UWI"'''
    # Define the possible alternative names for the well identifier column
    alternative_names = ["Well Unique Identifier", "CPA Pretty Well ID", "Well Identifier"]
    for alt_name in alternative_names:
        if alt_name in dataframe.columns:
            dataframe.rename(columns={alt_name: "UWI"}, inplace=True)



def get_point_info(wells, data, depth_type_to_query='md', col_name='MD'):
    '''# Iterate through the sample_data dataframe and calculate TVD for each sample
    wells = df of wells with uwi col
    col_name = name of col with depths inside data'''
    df = data.copy()
    
    def f(uwi, depth):
        well = get_col_UWI(wells, uwi, 'well')
        point_info = well.get_point(depth, depth_type_to_query)
        return point_info
    
    points_info = df.apply(lambda x: pd.Series(f(x['UWI'], x[col_name])), axis=1)

    if depth_type_to_query=='md':
        df['TVD'] = points_info['tvd']
    df['Easting'] = points_info['east']
    df['Northing'] = points_info['north']
    return df








# # Extract UWI, Northing, Easting, and elevation from collar
# UWI = collar_data['UWI']
# Northing = collar_data['Surf-Hole Northing (NAD83)']
# Easting = collar_data['Surf-Hole Easting (NAD83)']
# elevation = collar_data['Ground Elevation (m)']
# # Extract sample_midpoint_depth from survey
# midpoint = sample_data['sample_midpoint_depth']



#print(collar_data)
#print(survey_data)
# print(sample_data)
#print(UWI, midpoint)

surveys = import_survey(path, survey_csv)
collars = import_collar(path, collar_csv, surveys)



samples = import_sample(path, sample_csv, collars)
tops = import_geology(path, geology_csv, collars)

print("COLLARS")
print(collars)
print("SURVEYS")
print(surveys)
print("SAMPLES")
print(samples)
print("TOPS")
print(tops)
