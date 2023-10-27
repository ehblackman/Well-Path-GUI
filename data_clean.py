import well_profile as wp
import pandas as pd
from GUI_file_importer import main



def import_collar(collar_data, survey_data):
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
    
def import_survey(survey_data):
    # Preprocessing
    change_alternative_to_uwi(survey_data)
    # Convert the "UWI" column to string data type in survey_data
    survey_data['UWI'] = survey_data['UWI'].astype(str)

    survey_data = survey_data.rename(columns={'Azimuth Angle': 'azi'})
    survey_data = survey_data.rename(columns={'Inclination': 'inclination'})
    survey_data = survey_data.rename(columns={'Measured Depth': 'md'})

    return survey_data

def import_sample(sample_data, collar_data):  
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

def import_geology(geology_data, collar_data):
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
if __name__ == "__main__":
    collar_data, survey_data, sample_data, geology_data = main()
    surveys = import_survey(survey_data)
    collars = import_collar(collar_data, surveys)
    
    
    
    samples = import_sample(sample_data, collars)
    tops = import_geology(geology_data, collars)
    
    print("COLLARS")
    print(collars)
    print("SURVEYS")
    print(surveys)
    print("SAMPLES")
    print(samples)
    print("TOPS")
    print(tops)
