from classes import Collar, Well, Survey, Sample
import well_profile as wp
import pandas as pd


# File import
path = 'test well data'
collar_csv = 'Collar GUI.csv'
survey_csv = 'Survey GUI.csv'
sample_csv = 'Sample GUI.csv'

# Load collar, survey & sample data from CSV files to pandas dataframes
collar_data = pd.read_csv(f'{path}/{collar_csv}')
survey_data = pd.read_csv(f'{path}/{survey_csv}')
sample_data = pd.read_csv(f'{path}/{sample_csv}')

# Extract UWI, latitude, longitude, and elevation from collar
latitude = collar_data['Surf-Hole Latitude (NAD83)']
longitude = collar_data['Surf-Hole Longitude (NAD83)']
elevation = collar_data['Ground Elevation (m)']


# Define the possible alternative names for the well identifier column
alternative_names = ["Well Unique Identifier", "CPA Pretty Well ID", "Well Identifier"]

# Function to change alternative column names to "UWI"
def change_alternative_to_uwi(dataframe):
    for alt_name in alternative_names:
        if alt_name in dataframe.columns:
            dataframe.rename(columns={alt_name: "UWI"}, inplace=True)

# Call the function to change column names
#This means we can use UWI as the well name across dataframes
change_alternative_to_uwi(collar_data)
change_alternative_to_uwi(survey_data)
change_alternative_to_uwi(sample_data)


print(collar_data)
print(survey_data)
print(sample_data)