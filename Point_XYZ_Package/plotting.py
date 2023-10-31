import plotly.graph_objects as go

def plot(collar_data, sample_data):
    # Create a single figure to hold all well plots and sample data
    fig = go.Figure()

   # Iterate through all wells
    for uwi in collar_data['UWI'].unique():
        data = collar_data[collar_data['UWI'] == uwi]
        well_fig = data['well'].iloc[0].plot()  # Assuming "plot" method is used to visualize well
        for trace in well_fig['data']:
            fig.add_trace(trace)  # Add all traces of the well plot to the main figure


    # Plot samples for all wells
    for uwi in collar_data['UWI'].unique():
        data = sample_data[sample_data['UWI'] == uwi]
        x = data['Easting']
        y = data['Northing']
        z = data['Sample Depth Below Sea Level']
        fig.add_trace(
            go.Scatter3d(x=x, y=y, z=z,
                         marker=dict(color='red', size=5),
                         line=dict(width=0),
                         name=f'Sample - {uwi}'))

    # Show the combined figure with all well plots and sample data
    fig.show()
