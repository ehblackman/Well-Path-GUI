import pandas as pd
import well_profile as wp


# File import geology tops
path = 'test well data'
geology_csv = 'Geology GUI.csv'
# Load collar, survey & sample data from CSV files to pandas dataframes
geology_data = pd.read_csv(f'{path}/{geology_csv}', skiprows=15)


# Define the possible alternative names for the well identifier column
alternative_names = ["Well Unique Identifier", "CPA Pretty Well ID", "Well Identifier"]

# Function to change alternative column names to "UWI"
def change_alternative_to_uwi(dataframe):
    for alt_name in alternative_names:
        if alt_name in dataframe.columns:
            dataframe.rename(columns={alt_name: "UWI"}, inplace=True)

# Call the function to change column names
#This means we can use UWI as the well name across dataframes
change_alternative_to_uwi(geology_data)

# Convert the "UWI" column to string data type in collar_data
geology_data['UWI'] = geology_data['UWI'].astype(str)


# Iterate through the sample_data dataframe and calculate TVD for each sample
depth_to_query = geology_data['TVD']
depth_type_to_query = 'tvd'

well = wp.load(f'{path}/{geology_csv}')   

points_info = depth_to_query.apply(lambda d: pd.Series(well.get_point(d, depth_type_to_query)))

geology_data['Longitude'] = points_info['east']
geology_data['Latitude'] = points_info['north']

# Add ground elevation to sample data
geology_data['Ground Elevation'] = geology_data['UWI'].apply(lambda u: collar_data.loc[collar_data['UWI']==u]['Ground Elevation (m)'])
geology_data['Sample Depth Below Sea Level'] = geology_data['Ground Elevation'] - geology_data['TVD']

print(geology_data)