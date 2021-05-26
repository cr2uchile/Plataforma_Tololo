#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:50:56 2021

@author: sebastian
"""
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import geopandas as gpd
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os as os
import numpy as np
import datetime
import base64
from datetime import date
from datetime import timedelta
from textwrap import dedent
from datetime import datetime as dt
from scipy.optimize import leastsq
from __toolsTrend import *
from __TrendGraphs import *
from __MonthHourGraphs import *
from __BoxplotGraphs import *
from __HistGraphs import *


orig = os.getcwd()
fn_dmc = os.path.join(orig,'DATA','DMC-O3_RH_1H_dmc-1995-2013_clear.csv')
DMC_data = pd.read_csv(fn_dmc, index_col=0, parse_dates=True)
fn_ebas = os.path.join(orig,'DATA','EBAS-O3H-2013-2019.csv')
EBAS_data = pd.read_csv(fn_ebas, parse_dates=True, index_col=0)
EBAS_data.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

image_filename_cr2 = 'logo_footer110.png'
encoded_image_cr2 = base64.b64encode(open(image_filename_cr2, 'rb').read()).decode('ascii')
image_filename_cr2_celeste = 'cr2_celeste.png'
encoded_image_cr2_celeste = base64.b64encode(open(image_filename_cr2_celeste, 'rb').read()).decode('ascii')
image_filename_DMC = 'logoDMC_140x154.png'
encoded_image_DMC = base64.b64encode(open(image_filename_DMC, 'rb').read()).decode('ascii')
image_filename_tololo = 'Tololo.png'
encoded_image_tololo = base64.b64encode(open(image_filename_tololo, 'rb').read()).decode('ascii')
image_filename_tololo_download = 'Tololo_Download.png'
encoded_image_tololo_download = base64.b64encode(open(image_filename_tololo_download, 'rb').read()).decode('ascii')
image_filename_GWA = 'gaw_logo.png'
encoded_image_GWA = base64.b64encode(open(image_filename_GWA, 'rb').read()).decode('ascii')
image_filename_lamsal = 'grafico_aero.png'
encoded_image_lamsal = base64.b64encode(open(image_filename_lamsal, 'rb').read()).decode('ascii')


##############cosas del mapa


fig = go.Figure(go.Scattergeo(lat=[-30.169], lon=[-70.804]))
fig.update_geos(projection_type="orthographic", projection_rotation=dict(lon=-80, lat=-30), bgcolor='rgba(0,0,0,0)',
                lataxis_showgrid=True, lonaxis_showgrid=True
                
                  )
fig.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}, 
                  plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6')



d = {'City':'Tololo', 'lat' : -30.169, 'lon': -70.804 , 'State': 'Valle del elqui' ,'info': 'Observatorio Interamericano del Cerro Tololo','MSL':2200}
cites = pd.DataFrame(data=d, index = [0])

fig2 = px.scatter_mapbox(cites, lat="lat", lon="lon", hover_name="City", hover_data=["State", "info"],
                        color_discrete_sequence=["black"], size='MSL' , size_max=12 ,zoom=7, height=300 )
fig2.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
fig2.update_layout(margin={"r":10,"t":0,"l":10,"b":0})
fig2.update_mapboxes(bearing=25, pitch = 60)
#######################
### -tabs prperties
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'color': '#0668a1',
}

tab_selected_style = {
    'borderTop': '#1766a0',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1766a0',
    'color': 'white',
    'padding': '6px'
}
###
colors = {
    'background': 'white',
    'text': '#7FDBFF',
    'background_2': 'white',
    'background_3': 'cyan'

}
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
app.scripts.append_script({ 'external_url' : mathjax })

app.layout = html.Div([
################################### Configuración Encabezado Página Web##############    
    html.Div([
        html.Div([html.H2("Tololo Ozone Measurements", style={'font-size':'18pt','color': 'white','font-family': 'Abel', 'font-weight': '200 !important', 'margin-top': '28px', 'margin-left':'10px'})], style={'position':'absolute','display': 'inline-block'}),
             html.A([       
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_cr2), style={'height':'80px'})],href = 'http://www.cr2.cl/', style={'margin-left': '400px', 'position':'absolute'}),
             html.A([     
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_DMC),style = {'height':'80px'})], href='http://www.meteochile.gob.cl/PortalDMC-web', style={'margin-left': '700px', 'position':'absolute'}),
             html.A([     
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_GWA),style = {'height':'80px'})], href='https://www.wmo.int/gaw/', style={'margin-left': '900px', 'position':'absolute'}),
             html.Div([
                 html.H2("Language:" , style={'font-size':'15pt','color': 'white', 'margin-top': '30px'})], style={'margin-left': '1050px','display': 'inline-block', 'position':'absolute'}
                 ),
            html.Div([
                daq.ToggleSwitch(
                    id='Switch_Lang',
                    className='SwicthLang',
                    value=True,
                    )], style={'backgroundColor':'#1766a0','margin-top':'30px','margin-left': '1150px','display': 'inline-block', 'position':'absolute'}) 
    ],
    style={'backgroundColor':'#1766a0', 'height':'80px'}),
#####################################################################################    
    html.Div(id='tabs-content', style={'backgroundcolor':'#f6f6f6'})
])
########################################Contenido Página Web#########################
@app.callback(Output('tabs-content', 'children'),
              Input('Switch_Lang', 'value'))
def Web_Language(Switch_Lang):
#####################################Versión en Ingles###############################    
    if Switch_Lang==False:
        return [html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Information',
                value='tab-1',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Graphs',
                value='tab-2',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Download Data',
                value='tab-3', className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Methods',
                value='tab-4',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes', style={'backgroundColor':'#f6f6f6'})
])]
#######################################Version en Español ##########################      
    if Switch_Lang==True:
        return [html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Presentación',
                value='tab-1',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Gráficos',
                value='tab-2',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Descargar Datos',
                value='tab-3', className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Métodos',
                value='tab-4',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes', style={'backgroundColor':'#f6f6f6'})
])]
    
@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'),
              Input('Switch_Lang', 'value'))
def render_content(tab, Switch_Lang):
################################################Tab 1###################################  
    if tab == 'tab-1':
        if Switch_Lang==False:
################################################ Informacion en Ingles##################            
            return [html.Div([html.Div([html.H1("Tololo (30.169 S, 70.804 W, 81m)", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'})
                ,dcc.Markdown(dedent(f'''
                Cerro Tololo (30ºS, 70ºW, 2200 m a.s.l.) is located about 50 km east of the Chilean coast at 30°S, where the cities of La Serena and Coquimbo are located. Smaller towns are situated nearby: Vicuña 20 km NE, Paiguano 30 km NE, Andacollo 30 km SW, Ovalle 60 km SW, see Error: no se encontró el origen de la referencia). The Elqui-Valley lies some 15 km N of Tololo in a W-E elongation, which is dominated by agricultural activity. The site is situated within the premises of the Interamerican Southern Astronomical Observatory. The topography of the area can be described as overly complex. The valleys around these mountains are deep, down to 500 m a.s.l., and the Andes mountain range is only 30 km east of Cerro Tololo with heights of up to 6 km a.s.l.
                Cerro Tololo most of the time is immersed in the free atmosphere and affected by the subsidence regime of the South Pacific high that brings clear sky conditions most of the year. In winter, the subtropical jet stream (STJ) is located on average at 30ºS. Above 4 km a.s.l., large-scale westerly winds prevail, while northerly winds are observed in a band between 2 and 4 km a.s.l., which results from the blocking effect of the westerly flow by the Andes. The In addition to these features, up-slope (down-slope) winds develop during the afternoon (night) at Tololo.

                Principal Investigators: Laura Gallardo, Carmen Vega        
                Emails: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl), [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
    
                
                Data Site Manager: Francisca Muñoz, CR2 – Center for Climate and Resilience Research.            
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Camilo Menares, CR2 - Center for Climate and Resilence Research.          
                Email: [cmenares@dgf.uchile.cl](mailto:cmenares@dgf.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Sebastian Villalón, CR2 - Center for Climate and Resilence Research.             
                Email: [sebastian.villalon@ug.uchile.cl](mailto:sebastian.villalon@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data Disclaimer: These data have been collected at Tololo by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).
    
                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                
                
                '''), style={'margin-left':'60px'})] ,  
                style={'color': 'black', 'width':'50%',
                                                    'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px', 'margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'}), dcc.Markdown('Credits: NOAO/NSF/AURA', style={'margin-left':'75px'}),
                                    html.H1("Map", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig) , 
                                    html.H1("Interactive map", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),                                     
                                    dcc.Graph(figure=fig2)],
                                    
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%', 'backgroundColor': '#f6f6f6'})
                              ], style={'backgroundColor': '#f6f6f6', 'height':'780px'})
                              ]
#################################################Informacion en Español#####################################                              
        elif Switch_Lang==True:
            return[
                html.Div([
                html.Div([html.H1("Tololo (30.169 S, 70.804 W, 81m)", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             dcc.Markdown(dedent(f'''
                Como parte del programa  Global Atmospheric Watch (GAW), la Organización Meteorológica Mundial instaló una estación de monitoreo de radiación y ozono superficial en el Observatorio Interamericano Cerro Tololo, ubicado próximo a la ciudad de La Serena en Chile. Además, con el objetivo del programa “QHAWAYRA” (en quechua  “estudio del aire”) esta localidad fue adecuada como una estación de GAW completamente equipada (Gallardo et al. 2000). Las mediciones de  GAW describen cambios a largo plazo en las condiciones atmosféricas. Este objetivo requiere medir en sitios libre de impacto por fuentes antropogénicas o en lugares donde sea identificado de manera que los datos puedan diferenciarse de su influencia. Por esta razón, las ubicaciones de estas estaciones a veces se eligen en cumbres de altas montañas como Cerro Tololo. Cerro Tololo (2200 m sobre el nivel medio del mar (MSL)) se encuentra a unos 50 km al este de la costa chilena a 30 ° S, donde se encuentran las ciudades de La Serena y Coquimbo. La topografía del área puede describirse como compleja. Los valles alrededor de estas montañas son profundos, hasta 500 m MSL, y la cordillera de los Andes está a solo 30 km al este del Cerro Tololo con alturas de hasta 6 km MSL.
                                                 
                Investigadoras Principales: Laura Gallardo, Carmen Vega
                Correos electrónicos: [lgallard@u.uchile.cl] (mailto: lgallard@u.uchile.cl), [carmen.vega@dgac.gob.cl] (mailto: carmen.vega@dgac.gob.cl)
         
                
                Responsable del sitio: Francisca Muñoz, CR2 - Centro de Investigación sobre Clima y Resiliencia.
                Correo electrónico: [fmunoz@dgf.uchile.cl] (mailto: fmunoz@dgf.uchile.cl)
                AV. Blanco Encalada 2002, Santiago, Chile
                
                Científico de datos: Camilo Menares, CR2 - Centro de Investigación en Clima y Resilencia.
                Correo electrónico: [cmenares@dgf.uchile.cl] (mailto: cmenares@dgf.uchile.cl)
                AV. Blanco Encalada 2002, Santiago, Chile
                
                Científico de datos: Sebastián Villalón, CR2 - Centro de Investigación sobre Clima y Resilencia.
                Correo electrónico: [sebastian.villalon@ug.uchile.cl] (mailto: sebastian.villalon@ug.uchile.cl)
                AV. Blanco Encalada 2002, Santiago, Chile
                
                Descargo de responsabilidad sobre los datos: estos datos han sido recopilados en Tololo por la Oficina Meteorológica de Chile (DMC) bajo los auspicios del Programa de Vigilancia Atmosférica Global (GAW) de la Organización Meteorológica Mundial (OMM).

                Los datos de este sitio web están sujetos a revisión y reprocesamiento. Consulta las fechas de creación para descargar la versión más actual.
    
                Comuníquese con el investigador principal de la estación si tiene preguntas sobre las técnicas y la calidad de los datos.
                
                '''), style={'margin-left':'60px'})] ,  
                style={'color': 'black', 'width':'50%','backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px','margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'}), dcc.Markdown('Créditos: NOAO/NSF/AURA', style={'margin-left':'75px'}),
                                    html.H1("Mapa", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig) , 
                                    html.H1("Mapa interactivo", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),                                     
                                    dcc.Graph(figure=fig2)],
                                    
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%', 'backgroundColor': '#f6f6f6'})
                ], style={'backgroundColor': '#f6f6f6', 'height':'780px'})
                                          ]
#####################################################################################
    elif tab == 'tab-2':
        if Switch_Lang==False:
                return [html.Div([
                    html.Div([
                    
                html.H1("Trends", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
        html.Div([html.Label('Trends: ', style={'color':'#0668a1','display': 'inline-block'}),
                  html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Lamsal", "value": "Lamsal"},
                {"label": "EMD", "value": "EMD"},
                {"label": "Linear", "value": "Linear"},
                {"label": "ThielSen", "value":"ThielSen"},
                {"label": "STL", "value":"STL"}
            ],
            id="radio_trends",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Lamsal"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'})
                 ,
                  
        html.Label('Period: ', style={'color':'#0668a1','display': 'inline-block'}),
                  html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Daily", "value": "Daily"},
                {"label": "Monthly", "value": "Monthly"}
            ],
            id="radio_trends_period",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Daily"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'})
                 
                  ])
        ,
        dcc.Graph(id='Trend_graph', figure={"layout":{"height":400, "width":1080}})], style={'margin':'auto','width':'1080px', 'height':'500px'}),
        html.Div([
            html.Div([
    html.H1("Month-Hour Diagram", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
    html.Div([ html.Label('Date Range:', style={'color':'#0668a1','font-size':'18px', 'backgroundColor':'#f6f6f6'}),
            dcc.DatePickerRange(
                id='calendar_1',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'margin-left':'50px'}),
        dcc.Graph(id="MonthHourDiagram", style={'backgroundColor':'#f6f6f6'})], style={'margin-left':'100px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block'})
        ], style={'display':'inline-block'}),
        html.Div([
                daq.ToggleSwitch(
                    className='SwitchHBENG',
                    id='Switch_ENG',
                    value=False,
                    )   
                    , html.Div(id='switch-content')], style={'margin-left':'5px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block', 'backgroundColor':'#f6f6f6'})
        ,
        
    ], style={'backgroundColor': '#f6f6f6', 'height':'1100px'})
                    ]
        
        if Switch_Lang==True:
            return [
################################################GRafico Tendencia################
                html.Div([                
                html.Div([html.H1("Tendencia", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                              html.Div([
    html.Div([html.Label("Tendencia:", style={'font-size':'18px', 'color':'#0668a1'})],style={'display':'inline-block'}), html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Lamsal", "value": "Lamsal"},
                {"label": "EMD", "value": "EMD"},
                {"label": "Linear", "value": "Linear"},
                {"label": "ThielSen", "value":"ThielSen"},
                {"label": "STL", "value":"STL"}
            ],
            id="radio_trends_esp",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Lamsal"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'}), 
    html.Label('Periodo: ', style={'color':'#0668a1','display': 'inline-block'}),
                  html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Diario", "value": "Diario"},
                {"label": "Mensual", "value": "Mensual"}
            ],
            id="radio_trends_period_esp",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Diario"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'})
    
    
    ]),
            
            dcc.Graph(id='Tendencia_graf', figure={"layout":{"height":400, "width":1080}})], style={'margin':'auto','width':'1080px', 'height':'500px'}),
                
            html.Div([
                html.Div([
                html.H1("Diagrama Mes-Hora", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}), 
                html.Div([ html.Label('Intervalo de Tiempo:', style={'color':'#0668a1','font-size':'18px', 'backgroundColor':'#f6f6f6'}),
            dcc.DatePickerRange(
                id='calendario_1',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'margin-left':'50px'}),dcc.Graph(id="DiagramaMesHora", style={'backgroundColor':'#f6f6f6'})], style={'margin-left':'100px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block', 'backgroundColor':'#f6f6f6'}
                ),
                html.Div([
                daq.ToggleSwitch(
                    id='Switch',
                    className='SwitchHBESP',
                    value=False,
                    )   
                    , html.Div(id='switch-contenido')], style={'margin-left':'5px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block'})
                ])
        ], style={'backgroundColor': '#f6f6f6', 'height':'1100px'})    
        ]
    elif tab == 'tab-3':
        if Switch_Lang==False:
            return html.Div([
                html.Div([html.H1("Download", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),dcc.Markdown(dedent(f''' You can download the measurements at the Tololo station. In case you need a specific time interval, you must select the dates in the calendar and then press the download button:
                '''), style={'margin-left':'60px'}),dcc.DatePickerRange(
                id='calendario_descarga',
                start_date=min(DMC_data.index),
                end_date=max(EBAS_data.index)
                , style={'margin-left':'60px'}) ,dbc.Button("Descargar ", id="btn_descarga_2", n_clicks=0, style={'margin-left':'5px','display':'inline-block', 'backgroundColor':'#0668a1'}),Download(id="download_2")
                ,dcc.Markdown(dedent(f''' CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.'''
                    ), style = {'margin-top':'50px', 'margin-left':'60px'}) 
                
                ],style={'color': 'black', 'width':'50%', 'margin-left':'0px'
                                                    ,'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo_download), 
                                   style={'width':'350px' ,'margin-left':'70px','margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'})    
                    ], style={'display':'inline-block','float':'right' ,'width':'50%'})
                               
                               ], style={'backgroundColor': '#f6f6f6','height': '650px'})
                
            
        elif Switch_Lang==True:
            return html.Div([
        html.Div([html.H1("Descarga", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),dcc.Markdown(dedent(f''' A continuación usted podrá descargar las mediciones realizadas en la estación Tololo. En el caso de una periodo especifico debe seleccionar las fechas en el calendario y a continuación presionar el botón de descargas:
                '''), style={'margin-left':'60px'}),dcc.DatePickerRange(
                id='calendario_descarga',
                start_date=min(DMC_data.index),
                end_date=max(EBAS_data.index)
                , style={'margin-left':'60px'}) ,dbc.Button("Descargar ", id="btn_descarga_2", n_clicks=0, style={'margin-left':'5px','display':'inline-block', 'backgroundColor':'#0668a1'}),Download(id="download_2")
                ,dcc.Markdown(dedent(f''' CITA: Si usted utiliza este conjunto de datos, comuníquese con la Oficina Meteorológica de Chile y cite Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.'''
                    ), style = {'margin-top':'50px', 'margin-left':'60px'}) 
                
                ],style={'color': 'black', 'width':'50%', 'margin-left':'0px'
                                                    ,'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo_download), 
                                   style={'width':'350px' ,'margin-left':'70px','margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'})    
                    ], style={'display':'inline-block','float':'right' ,'width':'50%'})
                               
                               ], style={'backgroundColor': '#f6f6f6','height': '650px'})
    elif tab == 'tab-4':
        if Switch_Lang==False:
            return [html.Div([
                
                html.H1("Data", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f''' 
                        In 1995, TLL has been equipped with an ozone photometer and a set of meteorological sensors. Ozone at TLL is
                        measured by UV absorption with a Thermo Environmental Instruments Inc. TECO 49-003 analyzer. The station is
                        equipped with an external ozonator which allows producing defined levels of ozone to conduct performance checks.
                        Measurements are done continuously and data are recorded
                        on a Campbell Scientific 21X data logger as 15 min averages. Zero and span checks on multiple levels are done twice
                        weekly and once monthly, respectively, to keep track of the
                        background signal and the instrument response. Regularly,
                        the operator visually inspects the recorded data for obvious
                        anomalies.                '''), 
                
                style={'margin-left':'60px'}) ,
                
                html.H1("Quality assurance and quality control", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f''' 
                            The raw data has been processed following quality control criteria.                             
                            K-Nearest Neighbors filter to detect calibration lines, this algorithm is configured with k = 3 nearest neighbors and a Euclidean distance 
                            defined as three standard deviations.                                 
                            Filter extreme percentiles (0.01 and 0.99) of the distribution to remove outliers.                                Instrumental filter, based on the lower detection limit of the ozone measurement.                                Daily and monthly averages are generated only when 70% of the data is available,
                '''), 
                
                style={'margin-left':'60px'}) ,
#                 html.H1("Back trajectories", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
# #                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
#                 dcc.Markdown(dedent(f'''
#                                     Not available                '''), 
                
#                  style={'margin-left':'60px'}) ,

                html.H1("Trends", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f'''
                Trends were calculated using several methods found in the literature. These methods are summarized below:

                                                   
                **STL:**
                This method  (Cleveland et al. 1990) of decomposing signals uses Loess techniques to generate local smoother functions. Then by decoupling the seasonality and separating the noise obtaining a monotonic function for the trend. Cleveland et al. 1990 
               
                **EMD**
                In this method (Huang et al. 1998), the signal is decomposed as a superposition of local sums of oscillatory components called Intrinsic Mode Functions (IMF). The IMF modes added to a function without oscillatory components reconstruct the original signal. 
                
                **Lamsal-Fourier:**
                This method (Lamsal et al. 2015) uses a multilinear regression model based on harmonic functions (Fourier regression) to determine the components in the linear trends.                

                **Thiel Sen:**
                In the Theil-Sen method (Theil 1992, Sen 1960), multiple slopes are calculated to select the final slope as the median of all these
                '''), 
                
                style={'margin-left':'60px'}) ,
                                        
                            
            ], style={'width':'50%', 'display':'inline-block', 'margin-top':'50px'}), 
                                    html.Div([
                html.H1("Paper Tololo", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
                Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.
                
                Gallardo, L., Carrasco, J., and Olivares, G. (2000). An analysis of ozone measurements at Cerro Tololo (30°S, 70°W, 2200 m.a.s.l.) in Chile. Tellus, Ser. B Chem. Phys. Meteorol. 52, 50–59. doi:10.3402/tellusb.v52i1.16081.
                
                
                Kalthoff, N., Bischoff-Gauß, I., Fiebig-Wittmaack, M., Fiedler, F., Thürauf, J., Novoa, E., et al. (2002). Mesoscale wind regimes in Chile at 30°S. J. Appl. Meteorol. 41, 953–970. doi:10.1175/1520-0450(2002)041<0953:MWRICA>2.0.CO;2.
                
                Rondanelli, R., Gallardo, L., and Garreaud, R. D. (2002). Rapid changes in ozone mixing ratios at Cerro Tololo (30°10′S, 70°48′W, 2200 m) in connection with cutoff lows and deep troughs. J. Geophys. Res. Atmos. 107, ACL 6-1-ACL 6-15. doi:10.1029/2001JD001334. 
                
               '''), style={'margin-left':'60px'}) ,
                html.H1("Paper Trend", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
                Cleveland, R., Cleveland, W., of official, J.M.J., undefined 1990,
                1990. STL: A seasonal-trend decomposition. nniiem.ru URL: http:
                //www.nniiem.ru/file/news/2016/stl-statistical-model.pdf .
                                    
                Huang, N.E., Shen, Z., Long, S.R., Wu, M.C., Snin, H.H., Zheng, Q., Yen, N.C., Tung, C.C., Liu, H.H., 1998. The empirical mode decom- position and the Hubert spectrum for nonlinear and non-stationary time series analysis. Proceedings of the Royal Society A: Mathemat- ical, Physical and Engineering Sciences 454, 903–995. doi: 10.1098/rspa.1998.0193 .
                                
                Lamsal, L.N., Duncan, B.N., Yoshida, Y., Krotkov, N.A., Pickering,K.E., Streets, D.G., Lu, Z., 2015. U.S. NO2 trends (2005–2013): EPA Air Quality System (AQS) data versus improved observations from the Ozone Monitoring Instrument (OMI). Atmospheric Environment 110, 130–143. URL: http://linkinghub.elsevier.com/re
                
                Sen, P.K., 1960. On Some Convergence Properties of U-Statistics. Calcutta Statistical Association Bulletin 10, 1–18. URL:https://journals.sagepub.com/doi/abs/10.1177/00
                
               '''), style={'margin-left':'60px'})
                ], style={'margin-top':'50px','display':'inline-block','float':'right' ,'width':'50%'})
                                    ]
                                    
                        
        if Switch_Lang==True:        
            return [html.Div([
                html.H1("Data", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f''' 
                        In 1995, TLL has been equipped with an ozone photometer and a set of meteorological sensors. Ozone at TLL is
                        measured by UV absorption with a Thermo Environmental Instruments Inc. TECO 49-003 analyzer. The station is
                        equipped with an external ozonator which allows producing defined levels of ozone to conduct performance checks.
                        Measurements are done continuously and data are recorded
                        on a Campbell Scientific 21X data logger as 15 min averages. Zero and span checks on multiple levels are done twice
                        weekly and once monthly, respectively, to keep track of the
                        background signal and the instrument response. Regularly,
                        the operator visually inspects the recorded data for obvious
                        anomalies.                '''), 
                
                style={'margin-left':'60px'}) ,
                
                html.H1("Calidad y control de datos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
#                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
               dcc.Markdown(dedent(f''' 
                            Los datos brutos se han procesado con los siguientes criterios de control de calidad.
                             Filtro K-Vecinos más cercanos para detectar líneas de calibración, este algoritmo está configurado con k = 3 vecinos más cercanos y una distancia euclidiana definida como tres desviaciones estándar. Filtre los percentiles extremos (0.01 y 0.99) de la distribución para eliminar los valores atípicos. Filtro instrumental, basado en el límite de detección inferior de la medición de ozono. Los promedios diarios y mensuales se generan solo cuando el 70% de los datos están disponibles.                '''), 
                
                style={'margin-left':'60px'}) ,
#                 html.H1("Back trajectories", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             
# #                html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$'), 
#                 dcc.Markdown(dedent(f'''
#                                     Not available                '''), 
                
#                  style={'margin-left':'60px'}) ,

                html.H1("Tendencias", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
                Las tendencias se calcularon utilizando varios métodos encontrados en la literatura. Estos métodos se resumen a continuación.
                
                
                **Seasonal and Trend decomposition using Loess (STL):**
                Este método (def en Cleveland et al. 1990) para descomponer señales, usa las técnicas de Loess con el fin de generar funciones smoother locales. Con esto desacopla la estacionalidad (Yt) y separa el ruido (Rt) obteniendo una función monótona para la tendencia (Tt).
                
                
                **Empirical Mode Decomposition (EMD):**
                EMD (Huang et al. 1998) es un método para analizar datos no lineales y no estacionarios. En este método, los datos o la señal se descomponen como una superposición de sumas locales de componentes oscilatorios denominados Funciones de modo intrínseco (IMF). Los modos IMF sumados a una función sin componentes oscilatorios  reconstruyen la señal original. 
                
                **Lamsal-Fourier:**
                Lamsal et al. 2015 utiliza un modelo de regresión multilineal basado en funciones armónicas para determinar los componentes en las tendencias lineales. La señal de frecuencia mensual es calculada como la suma de tres subcomponentes. Un regresión de fourier (α) de n componentes armonicas, un ruido (R) y una componente constante (β) multiplicada por el tiempo, esta ultima la tendencia de la señal.
                                
                '''), style={'margin-left':'60px'})
                
            ], style={'width':'50%', 'display':'inline-block', 'margin-top':'50px'}), html.Div([

                html.H1("Artículos Tololo", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
                Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.
                
                Gallardo, L., Carrasco, J., and Olivares, G. (2000). An analysis of ozone measurements at Cerro Tololo (30°S, 70°W, 2200 m.a.s.l.) in Chile. Tellus, Ser. B Chem. Phys. Meteorol. 52, 50–59. doi:10.3402/tellusb.v52i1.16081.
                
                
                Kalthoff, N., Bischoff-Gauß, I., Fiebig-Wittmaack, M., Fiedler, F., Thürauf, J., Novoa, E., et al. (2002). Mesoscale wind regimes in Chile at 30°S. J. Appl. Meteorol. 41, 953–970. doi:10.1175/1520-0450(2002)041<0953:MWRICA>2.0.CO;2.
                
                Rondanelli, R., Gallardo, L., and Garreaud, R. D. (2002). Rapid changes in ozone mixing ratios at Cerro Tololo (30°10′S, 70°48′W, 2200 m) in connection with cutoff lows and deep troughs. J. Geophys. Res. Atmos. 107, ACL 6-1-ACL 6-15. doi:10.1029/2001JD001334. 
                
               '''), style={'margin-left':'60px'}) ,
                html.H1("Artículos tendencia", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
                Cleveland, R., Cleveland, W., of official, J.M.J., undefined 1990,
                1990. STL: A seasonal-trend decomposition. nniiem.ru URL: http:
                //www.nniiem.ru/file/news/2016/stl-statistical-model.pdf .
                                    
                Huang, N.E., Shen, Z., Long, S.R., Wu, M.C., Snin, H.H., Zheng, Q., Yen, N.C., Tung, C.C., Liu, H.H., 1998. The empirical mode decom- position and the Hubert spectrum for nonlinear and non-stationary time series analysis. Proceedings of the Royal Society A: Mathemat- ical, Physical and Engineering Sciences 454, 903–995. doi: 10.1098/rspa.1998.0193 .
                                
                Lamsal, L.N., Duncan, B.N., Yoshida, Y., Krotkov, N.A., Pickering,K.E., Streets, D.G., Lu, Z., 2015. U.S. NO2 trends (2005–2013): EPA Air Quality System (AQS) data versus improved observations from the Ozone Monitoring Instrument (OMI). Atmospheric Environment 110, 130–143. URL: http://linkinghub.elsevier.com/re
                
                Sen, P.K., 1960. On Some Convergence Properties of U-Statistics. Calcutta Statistical Association Bulletin 10, 1–18. URL:https://journals.sagepub.com/doi/abs/10.1177/00 ''')

                , style={'margin-left':'60px'})
                ], style={'margin-top':'50px','display':'inline-block','float':'right' ,'width':'50%'})]                    
#################################### Trend Graph ###################    
@app.callback(Output('Trend_graph', 'figure'),
              Input('radio_trends', 'value'),
              Input('radio_trends_period', 'value')
              )
def update_graph(radio_trends,radio_trends_period):
    
    fig = trend(DMC_data, EBAS_data, radio_trends,radio_trends_period, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)  

    return fig
########################################Grafico de Tendencia###################
@app.callback(Output('Tendencia_graf', 'figure'),
              Input('radio_trends_esp', 'value'),
              Input('radio_trends_period_esp', 'value')
              )
def update_graph(radio_trends_esp, radio_trends_period_esp):
    
    fig = tendencia(DMC_data, EBAS_data, radio_trends_esp,radio_trends_period_esp,encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)

    return fig

#################################Slider- Español##############################
@app.callback(Output('switch-contenido', 'children'),
              Input('Switch', 'value'))
def render_content(Switch):
    if Switch == False:
        return [html.Div([
    html.H1("Histograma", style={'font-size':'24px','text-align': 'center','color': '#0668a1','backgroundColor':'#f6f6f6'}),
    html.Div([html.Label('Intervalo de tiempo:', style={'color':'#0668a1','font-size':'15px'}),
            dcc.DatePickerRange(
                id='calendario_3',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'#f6f6f6'}),
    dcc.Graph(id="Histograma", style={'backgroundColor':'#f6f6f6'})], style={'width':'525px','height':'400px', 'display': 'inline-block', 'backgroundColor':'#f6f6f6'})]
    elif Switch == True:
        return [html.Div([    
        html.H1("Boxplot", style={'font-size':'24px','text-align': 'center','color': '#0668a1','backgroundColor':'#f6f6f6'}),   
    html.Div([
        html.Label('Fechas:', style={'color':'#0668a1','font-size':'15px'}),       
            dcc.DatePickerRange(
                id='calendario_2',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3),
                )
     ], style={'display':'inline-block'})
        
    ,html.Div([html.Label("Promedio:", style={'color':'#0668a1','font-size':'18px'}), 
    html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Horario", "value": "Horario"},
                {"label": "Mensual", "value": "Mensual"},
            ],
            id="radio_boxplot_esp",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Horario"
        ),
    ],
    className="p-3",
    )
    ], style={'display':'inline-block'})
    ], style={'display':'inline-block'})
            ,
    dcc.Graph(id="Boxplot_esp", style={'backgroundColor':'#f6f6f6'})],style={'width':'525px','height':'400px'} )]
#################################Slider-English##############################
@app.callback(Output('switch-content', 'children'),
              Input('Switch_ENG', 'value'))
def render_content(Switch_ENG):
    if Switch_ENG == False:
        return [html.Div([
    html.H1("Histogram", style={'font-size':'24px','text-align': 'center','color': '#0668a1','backgroundColor':'#f6f6f6'}),
    html.Div([html.Label('Dates:', style={'color':'#0668a1','font-size':'15px'}),
            dcc.DatePickerRange(
                id='calendar_3',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'#f6f6f6'}),
    dcc.Graph(id="Histogram", style={'backgroundColor':'#f6f6f6'})], style={'width':'525px','height':'400px', 'display': 'inline-block'})]
    elif Switch_ENG == True:
        return [html.Div([    
        html.H1("Boxplot", style={'font-size':'24px','text-align': 'center','color': '#0668a1','backgroundColor':'#f6f6f6'}),   
    html.Div([
        html.Label('Dates:', style={'color':'#0668a1','font-size':'15px'}),       
            dcc.DatePickerRange(
                id='calendar_2',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3),
                )
     ], style={'display':'inline-block'})
        
    ,html.Div([html.Label("Mean:", style={'color':'#0668a1','font-size':'18px'}), 
    html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Hourly", "value": "Hourly"},
                {"label": "Monthly", "value": "Monthly"},
            ],
            id="radio_boxplot_eng",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Hourly"
        ),
    ],
    className="p-3",
    )
    ], style={'display':'inline-block'})
    ], style={'display':'inline-block'})
            ,
    dcc.Graph(id="Boxplot_Eng", style={'backgroundColor':'#f6f6f6'})],style={'width':'525px','height':'400px'} )]    
########################################## Month Hour Diagram#################
@app.callback(
    Output('MonthHourDiagram', 'figure'),
      [Input('calendar_1', 'start_date'),
      Input('calendar_1', 'end_date')])
def update_graph(start_date, end_date):
 
    fig = MonthHour(DMC_data, EBAS_data, start_date, end_date, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig
#######################################Diagrama Mes Hora###################### 
@app.callback(
    Output('DiagramaMesHora', 'figure'),
      [Input('calendario_1', 'start_date'),
      Input('calendario_1', 'end_date')])
def update_graph(start_date, end_date):
 
    fig = MesHora(DMC_data, EBAS_data, start_date, end_date, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig
#######################################Boxplot#################################
@app.callback(
    Output('Boxplot_Eng', 'figure'),
      [Input('calendar_2', 'start_date'),
      Input('calendar_2', 'end_date'), 
      Input('radio_boxplot_eng', 'value')])
def update_graph(start_date, end_date, radio_boxplot_eng):
    fig = BoxENG(DMC_data, EBAS_data, start_date, end_date, radio_boxplot_eng, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig  

###################################Diagrama cajas y bigotes ###################
@app.callback(
    Output('Boxplot_esp', 'figure'),
      [Input('calendario_2', 'start_date'),
      Input('calendario_2', 'end_date'), 
      Input('radio_boxplot_esp', 'value')])
def update_graph(start_date, end_date, radio_boxplot_esp):
    fig = BoxESP(DMC_data, EBAS_data, start_date, end_date, radio_boxplot_esp, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig  
#####################################Histogram#################################
@app.callback(
    Output('Histogram', 'figure'),
      [Input('calendar_3', 'start_date'),
      Input('calendar_3', 'end_date')])
def update_graph(start_date, end_date):
    fig = HistENG(DMC_data, EBAS_data, start_date, end_date)    
    return fig  

#####################################Histograma###############################
@app.callback(
    Output('Histograma', 'figure'),
      [Input('calendario_3', 'start_date'),
      Input('calendario_3', 'end_date')])
def update_graph(start_date, end_date):
    fig = HistESP(DMC_data, EBAS_data, start_date, end_date)    
    return fig  
############### DEscarga de datos#############################################

@app.callback(Output("download_2", "data"), [Input("btn_descarga_2", "n_clicks"),Input('calendario_descarga', 'start_date'),
      Input('calendario_descarga', 'end_date')])
def generate_csv(n_clicks, start_date, end_date):
    if n_clicks==0:
        return None
    else:
        df_all = pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date].round(0).drop(['O3_ppbv_std'],axis=1)
        return send_data_frame(df_all.to_csv, filename="Tololo_Time_Series_Dates_Selected.csv")    
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)


                                                              
