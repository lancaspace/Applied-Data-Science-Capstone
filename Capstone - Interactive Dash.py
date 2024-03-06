# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                # Dropdown component
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40','value':'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value':'VAFB SLC-4E'},

                                    ],
                                    value='ALL', 
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),

                                html.Br(),
                                # Pie Chart Component
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=2500,
                                                value=[min_payload, max_payload]
                                                ),
                                #Scatter Chart Component
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

#Defining Pie Chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
                     names='Launch Site', 
                     title='Mission Success Distribution Across All Launch Site')
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']== entered_site]
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df,values='class count',names='class',title=f" Successful Launches for site {entered_site}")
        return fig



#Defnining Scatter chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider', component_property='value')])
def scatter(entered_site, payload):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                         title='Class & Payloads for Launches on All Sites')
        return fig
    else:
        filtered_df_site = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df_site, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                         title=f'Class & Payloads for Launch Pad -  {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
