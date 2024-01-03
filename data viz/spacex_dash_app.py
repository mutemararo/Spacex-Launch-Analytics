# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("C:/Users/HP/Downloads/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[
                                    {'label':'All Sites', 'value':'All'},
                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}
                                ],
                                value='All',
                                placeholder='Select Site'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'All':
        data = spacex_df.groupby('Launch Site')['class'].sum()
        fig = px.pie(values=data.values,
        names=data.index.values,
        title='Success for All Sites')
        return fig
    else:
        info = spacex_df[spacex_df['Launch Site'] == entered_site].value_counts('class')
        figure = px.pie(values=info.values, 
                        names=['Failure','Success'], 
                        title='Chart for {}'.format(entered_site))
        return figure
    # return the outcomes piechart for a selected site
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(selected_site, payload):
    color_map = {'v1.0':'red', 'v1.1':'black', 'FT':'green', 'B4':'blue', 'B5':'yellow'}
    b_color = spacex_df['Booster Version Category'].map(color_map)

    if selected_site == 'All':
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=spacex_df['Payload Mass (kg)'], y=spacex_df['class'], 
                         mode='markers', marker=dict(color=b_color)))

        fig.update_layout(title='payload vs class', xaxis_title='payload', yaxis_title='class')
        return fig
    else:
        figure = go.Figure()
        data = spacex_df[spacex_df['Launch Site'] == selected_site]
        figure.add_trace(go.Scatter(x=data['Payload Mass (kg)'], y=data['class'], 
                         mode='markers', marker=dict(color=b_color)))
        figure.update_layout(title='payload vs class for {}'.format(selected_site), xaxis_title='payload', yaxis_title='class')
        return figure

# Run the app
if __name__ == '__main__':
    app.run_server()
