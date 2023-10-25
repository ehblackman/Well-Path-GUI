from data_import import *
import plotly.graph_objects as go

survey_data = import_survey(path, survey_csv)
collar_data = import_collar(path, collar_csv, survey_data)
sample_data = import_sample(path, sample_csv, collar_data)
geology_data = import_geology(path, geology_csv, collar_data)

for well in collar_data['well']:
    fig = well.plot(names=['Test'])

# Plot samples
data = sample_data[sample_data['UWI']=='test-well2']
x = data['Easting'] 
y = data['Northing']
z = data['TVD']
fig.add_trace(
    go.Scatter3d(x=x, y=y, z=z, 
                    marker=dict(color='red',size=10),
                    line=dict(width=0),
                    name=f'Sample'))

# Show fig
fig.show()