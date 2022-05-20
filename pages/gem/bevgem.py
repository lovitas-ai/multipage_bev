from cgitb import text
from sre_parse import State
import dash
from dash import dcc, html ,callback
from dash.dependencies import Output, Input, State
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
df_03=pd.read_excel(r'pages\gem\befo_gem_kennzahl.xlsx')
df_03['AGS'] = df_03['AGS'].astype(str)
df_03['AGS'] = df_03['AGS'].str.zfill(8)



#Layout

layout = dbc.Container([
        dbc.Row([
            dbc.Col([ 
                    html.P(" ",className='text-left text-primary mb-4'),
                    html.H2("Kartenanalysen",className='text-left text-primary mb-4'),
                    dcc.Dropdown(id='gem_ken', options=['Durchschnittsalter','Einwohner','Geschlechterverhältnis','Jugendquotient','Altenquotient','Gesamtquotient','Bevölkerungsdichte'], value='Durchschnittsalter',className='dropdown'),
                    dcc.Slider(id='year_map_gem', min = 2011, max=2020,step =1, value=2020,className='slider',updatemode='drag', marks={
                               2011:'2011',2012:'2012',2013:'2013',2014:'2014',2015:'2015',2016:'2016',2017:'2017',2018:'2018',2019:'2019',2020:'2020',}),
                    #html.H2("Durchschnittsalter",className='text-left text-primary mb-4'),
                    html.H3("",id="header_card",className='text-left text-primary mb-4'),
                    dcc.Markdown('',mathjax=True, id="text_ken"),
                    ], width={'size':9,'offset':1,'order':1})
                ],justify = 'start'),       
        dbc.Row([
            dbc.Col([
                    dcc.Graph(id='graph_map_gem',figure={},className='divBorder'),
                    ], width={'size':6,'offset':1,'order':1}),
            dbc.Col([
                dbc.CardHeader("Zusätzliche Informationen:"),
                dbc.CardBody([html.P("Card title", className="card-title",id='cardname1'),
                            html.P('Example P', className='card-text', id='cardyear1'),
                            html.P('Example P', className='card-text', id='cardeinw1'),
                            html.P('Example P', className='card-text', id='cardmänner1'),
                            html.P('Example P', className='card-text', id='cardfrauen1'),
                            html.P('Example P', className='card-text', id='cardgeschl_v1'),
                            html.P('Example P', className='card-text', id='carddalter1'),
                                ],className="card border-secondary divBorder")
                    ], width={'size':3,'offset':0,'order':1}),
                ],justify = 'start'),
         dbc.Row([
            dbc.Col([
                    html.P('Example P', className='card-text', id='name_klick'),
                    html.Button("Download Excel", id="btn_xlsx"),
                    dcc.Download(id="download-dataframe-xlsx"),
        ], width={'size':7,'offset':1,'order':1})
        ],justify = 'start')
         ], fluid=True, className='body' )
 

@callback(
    Output(component_id='graph_map_gem', component_property='figure'),
    [Input(component_id='year_map_gem', component_property='value')],
    [Input(component_id='gem_ken', component_property='value')],
    prevent_initial_call=False
    )
def update_my_graph2(year_map_gem,gem_ken):
    dff_03_01 = df_03[(df_03["Jahr"]==(year_map_gem))]
    fig = px.choropleth(dff_03_01,featureidkey='properties.AGS', geojson=gem_map, locations='AGS', color=dff_03_01[gem_ken],range_color=(df_03[gem_ken].min(),df_03[gem_ken].max()),
                    projection="mercator",color_continuous_scale="Viridis", hover_name='Name')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text = 'Bayern',margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@callback(
    Output(component_id='header_card', component_property='children'),
    [Input(component_id='year_map_gem', component_property='value')],
    [Input(component_id='gem_ken', component_property='value')],
    prevent_initial_call=False
    )

def update_header(year_map_gem,gem_ken):
    text = str(gem_ken)+' im Jahr '+str(year_map_gem)
    return text


@callback(
    Output(component_id='text_ken', component_property='children'),
    [Input(component_id='gem_ken', component_property='value')],
    prevent_initial_call=False
    )

def update_text(gem_ken):
    if gem_ken=='Durchschnittsalter':
        erkl='''
        Das Durchschnittsalter ist das arithmetisches Mittel des Alters aller Personen dieser Gemeinde zu Jahresende. \n
          $Durchschnittsalter=\\frac{Alter\; *\; Anzahl\,der\,Personen\,in\,diesem\,Alter}{Gesamtbevö\;lkerung}$
          '''
    if gem_ken=='Geschlechterverhältnis':
        erkl='Geschlechterverhältnis Erklärung $Altersquotient=\\frac{Personen\,im Alter\,von\,65+}{Personen\,im\,Alter\,von\,20\,bis\,65}$'
    if gem_ken=='Jugendquotient':
        erkl='''
                Der Jugendquotient gibt an, wie viele Menschen unter 20 Jahre auf 100 Personen von 20 bis unter 65 Jahre kommen. Da die Altersgruppe der
                 Jüngeren nur 20 Jahrgänge umfasst, die der Bevölkerung im Erwerbsalter hingegen 45, sind die Jahrgänge im Durchschnitt gleich stark besetzt,
                  wenn der Jugendquotient bei 44 liegt (20/45*100). Ein Jugendquotient unter 44 besagt, dass die nachwachsende Generation dünner besetzt ist als
                   die derzeitige Bevölkerung im Erwerbsalter. \n 
                $Jugendquotient=\\frac{Bevö\;lkerung\,bis\,18\,Jahren}{Bevö\;lkerung\,20-64\,Jahre}$
            '''
    return erkl

#Die Variablen, deren Veränderung nicht zu einem triggern des Callbacks führen sollen, müssen mit State festgeschrieben werden. 
@callback(
    Output("download-dataframe-xlsx", "data"),
    State(component_id='year_map_gem', component_property='value'),
    State(component_id='name_klick', component_property='children'),
    Input(component_id="btn_xlsx",component_property= "n_clicks"),
    prevent_initial_call=True,
)
def download_filter(year,Name,n_clicks):
        dff_03_03 = df_03[((df_03["Jahr"]==(year)) & (df_03["Name"]==(Name)) )]
        print(year)
        print(Name)
        print(dff_03_03)
        year_name = str(year)
        name_name=f'Export_{Name}_{year_name}.xlsx'
        return dcc.send_data_frame(dff_03_03.to_excel, filename=name_name, sheet_name=year_name)    



@callback(
    Output(component_id='cardname1', component_property='children'),
    Output(component_id='cardyear1', component_property='children'),
    Output(component_id='cardeinw1', component_property='children'),
    Output(component_id='cardmänner1', component_property='children'),
    Output(component_id='cardfrauen1', component_property='children'),
    Output(component_id='cardgeschl_v1', component_property='children'),
    Output(component_id='carddalter1', component_property='children'),
    [Input(component_id='year_map_gem', component_property='value')],
    [Input(component_id='graph_map_gem', component_property='hoverData')],
    prevent_initial_call=False
)

def update_my_text(year,hov_data):
    if hov_data is None: 
        kreis_val=year
        year_val =year
        einw=year
        männer=year
        frauen =year
        geschl_v=year
        dalter=year
        return (f' Kreis: {kreis_val}', f' Jahr : {year_val}' ,f' Anzahl der Einwohner : {einw}',f' Anzahl Männer : {männer}',
            f' Anzahl Frauen : {frauen}',f' Geschlechterverhältnis: Auf 100 Frauen kommen {geschl_v} Männer',f' Durchschnittsalter : {dalter} Jahre' )
    else: 
        AGS_hov=hov_data['points'][0]['location']
        dff_03_02 = df_03[((df_03["Jahr"]==(year)) & (df_03["AGS"]==(AGS_hov)) )]
        kreis_val=hov_data['points'][0]['hovertext']
        year_val =year
        einw=dff_03_02.reset_index().at[0,'Einwohner']
        Geschlechterverhältnis=dff_03_02.reset_index().at[0,'Geschlechterverhältnis']
        Durchschnittsalter =dff_03_02.reset_index().at[0,'Durchschnittsalter']
        Jugendquotient=dff_03_02.reset_index().at[0,'Jugendquotient']
        Bevölkerungsdichte=dff_03_02.reset_index().at[0,'Bevölkerungsdichte']
        return (f' Gemeinde: {kreis_val}', f' Jahr : {year_val}' ,f' Anzahl der Einwohner : {einw}',f'  Durchschnittsalter : { Durchschnittsalter}',
            f' Jugendquotient : {Jugendquotient}',f' Geschlechterverhältnis: Auf 100 Frauen kommen {Geschlechterverhältnis} Männer',f' Bevölkerungsdichte in p/qkm : {Bevölkerungsdichte} ' )

@callback(
    Output(component_id='name_klick', component_property='children'),
    [Input(component_id='year_map_gem', component_property='value')],
    [Input(component_id='graph_map_gem', component_property='clickData')],
    prevent_initial_call=False
)

def update_my_text(year,click_data):
    if click_data is None: 
        return (f' Noch keine Gemeinde gewählt' )
    else: 
        kreis_val=click_data['points'][0]['hovertext']

        return (f'{kreis_val}' )