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

# Calculate and add a new column 'MidpointDepth' to sample_data
sample_data['sample_midpoint_depth'] = (sample_data['Interval Base(m)'] + sample_data['Interval Top(m)']) / 2
# Delete rows with missing 'Interval Top(m)' or 'Interval Base(m)' data in sample_data
sample_data = sample_data.dropna(subset=['Interval Top(m)', 'Interval Base(m)'])

# Now, the sample_data dataframe no longer contains rows with missing data

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

# Convert the "UWI" column to string data type in collar_data
collar_data['UWI'] = collar_data['UWI'].astype(str)
# Convert the "UWI" column to string data type in survey_data
survey_data['UWI'] = survey_data['UWI'].astype(str)
# Convert the "UWI" column to string data type in sample_data
sample_data['UWI'] = sample_data['UWI'].astype(str)


# Extract UWI, latitude, longitude, and elevation from collar
UWI = collar_data['UWI']
latitude = collar_data['Surf-Hole Latitude (NAD83)']
longitude = collar_data['Surf-Hole Longitude (NAD83)']
elevation = collar_data['Ground Elevation (m)']
# Extract sample_midpoint_depth from survey
midpoint = sample_data['sample_midpoint_depth']





#print(collar_data)
print(survey_data)
#print(sample_data)
#print(UWI, midpoint)

