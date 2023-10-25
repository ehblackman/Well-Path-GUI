from classes import Collar, Well, Survey, Sample
import well_profile as wp
import pandas as pd


# File import
path = 'test well data'
collar_csv = 'Collar GUI.csv'
survey_csv = 'Survey GUI.csv'
sample_csv = 'Sample GUI.csv'
geology_csv = 'Geology GUI.csv'

def import_collar(path, collar_csv):
    # Load collar from CSV files to pandas dataframes
    collar_data = pd.read_csv(f'{path}/{collar_csv}')

    # Preprocessing
    change_alternative_to_uwi(collar_data)
    # Call the function to change column names
    #This means we can use UWI as the well name across dataframes
    # Convert the "UWI" column to string data type in collar_data
    collar_data['UWI'] = collar_data['UWI'].astype(str)
    return collar_data

def import_survey(path, survey_csv):
    # Load data
    survey_data = pd.read_csv(f'{path}/{survey_csv}')

    # Preprocessing
    change_alternative_to_uwi(survey_data)
    # Convert the "UWI" column to string data type in survey_data
    survey_data['UWI'] = survey_data['UWI'].astype(str)

    survey_data = survey_data.rename(columns={'Azimuth angle': 'azimuth'})
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
    sample_data = get_point_info(collar_data, sample_data)

    # Add ground elevation to sample data
    sample_data['Ground Elevation'] = sample_data['UWI'].apply(lambda u: get_col_UWI(collar_data, u, 'Ground Elevation (m)'))
    sample_data['Sample Depth Below Sea Level'] = sample_data['Ground Elevation'] - sample_data['TVD']

    return sample_data

def import_geology(path, geology_csv, collar_data):
    # Load data
    geology_data = pd.read_csv(f'{path}/{geology_csv}', skiprows=15)
    change_alternative_to_uwi(geology_data)
    geology_data['UWI'] = geology_data['UWI'].astype(str)


    # Get tvd
    geology_data = get_point_info(collar_data, geology_data)

    # Add ground elevation to sample data
    geology_data['Ground Elevation'] = geology_data['UWI'].apply(lambda u: get_col_UWI(collar_data, u, 'Ground Elevation (m)'))
    geology_data['Sample Depth Below Sea Level'] = geology_data['Ground Elevation'] - geology_data['TVD']

    return geology_data
    
def get_col_UWI(df, uwi, col):
    return df.loc[df['UWI']==uwi][col][0]

def change_alternative_to_uwi(dataframe):
    '''# Function to change alternative column names to "UWI"'''
    # Define the possible alternative names for the well identifier column
    alternative_names = ["Well Unique Identifier", "CPA Pretty Well ID", "Well Identifier"]
    for alt_name in alternative_names:
        if alt_name in dataframe.columns:
            dataframe.rename(columns={alt_name: "UWI"}, inplace=True)



def get_point_info(wells, sample_data, depth_type_to_query='md'):
    '''# Iterate through the sample_data dataframe and calculate TVD for each sample
    wells = df of wells with uwi col'''
    df = sample_data.copy()
    points_info = df.apply(lambda x: pd.Series(get_col_UWI(wells, x['UWI'], 'well').get_point(x['TVD'], depth_type_to_query)), axis=1)
    if depth_type_to_query=='md':
        df['TVD'] = points_info['tvd']
    df['Longitude'] = points_info['east']
    df['Latitude'] = points_info['north']
    return df








# # Extract UWI, latitude, longitude, and elevation from collar
# UWI = collar_data['UWI']
# latitude = collar_data['Surf-Hole Latitude (NAD83)']
# longitude = collar_data['Surf-Hole Longitude (NAD83)']
# elevation = collar_data['Ground Elevation (m)']
# # Extract sample_midpoint_depth from survey
# midpoint = sample_data['sample_midpoint_depth']



#print(collar_data)
#print(survey_data)
# print(sample_data)
#print(UWI, midpoint)

collar_data = import_collar(path, collar_csv)
well = wp.load(f'{path}/{survey_csv}')   
collar_data['well'] = [well]
import_survey(path, survey_csv)
import_sample(path, sample_csv, collar_data)
import_geology(path, geology_csv, collar_data)