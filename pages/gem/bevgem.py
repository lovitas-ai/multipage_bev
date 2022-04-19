from cgitb import text
import dash
from dash import dcc, html ,callback
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as gp
import numpy as np
import pandas as pd
import plotly.express as px
import geopandas

#
dash.register_page(__name__)

#Data
gem_map=geopandas.read_file('pages\gem\gemeinden.geojson') 
df_03=pd.read_csv('pages\gem\gemeinden.csv')
df_03['AGS'] = df_03['AGS'].astype(str)
df_03['AGS'] = df_03['AGS'].str.zfill(8)


#Layout

layout = dbc.Container([
        dbc.Row([
            dbc.Col([ 
                    html.P(" ",className='text-left text-primary mb-4'),
                    html.H2("Kartenanalysen",className='text-left text-primary mb-4'),
                    dcc.Slider(id='year_map_gem', min = 2018, max=2020,step =1, value=2020,className='slider',updatemode='drag', marks={
                    2018:'2018',2019:'2019',2020:'2020',}),
                    html.H2("Durchschnittsalter",className='text-left text-primary mb-4'),
                    dcc.Graph(id='graph_map_gem',figure={},className='divBorder'),
            ], width={'size':9,'offset':1,'order':1})
        ],justify = 'start')
         ], fluid=True, className='body' )


@callback(
    Output(component_id='graph_map_gem', component_property='figure'),
    [Input(component_id='year_map_gem', component_property='value')],
    prevent_initial_call=False
    )
def update_my_graph2(year_map_gem):
    dff_03_01 = df_03
    fig = px.choropleth(dff_03_01,featureidkey='properties.AGS', geojson=gem_map, locations='AGS', color=str(year_map_gem),
                    projection="mercator",color_continuous_scale="Viridis", hover_name='Name')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text = 'Bayern',margin={"r":0,"t":0,"l":0,"b":0})
    return fig



