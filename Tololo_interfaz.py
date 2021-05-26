# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 17:26:54 2021

@author: Sebastián
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
import dash_bootstrap_components as dbc
orig = os.getcwd()
fn_dmc = orig+'\\DATA\\'+'DMC-O3_RH_1H_dmc-1995-2013_clear.csv'
DMC_data = pd.read_csv(fn_dmc, index_col=0, parse_dates=True)
fn_ebas = orig+'\\DATA\\'+'EBAS-O3H-2013-2019.csv'
EBAS_data = pd.read_csv(fn_ebas, parse_dates=True, index_col=0)
EBAS_data.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
def completitud(df, n, frec):
    bad_mean = np.isnan(df.O3_ppbv).astype(int).resample(frec).sum()
    m = np.isnan(df.O3_ppbv).astype(int).resample(frec).sum().max()
    good_mean = bad_mean > m-n
    count_bad = good_mean.sum()
    df_hourly = df.resample(frec).mean()
    df_hourly[good_mean] = np.nan
    return [df_hourly, count_bad]
#-----------------------------------------------------------------------------
    
image_filename_top = '[www.cr2.cl][151]header_full.png'
encoded_image_top = base64.b64encode(open(image_filename_top, 'rb').read()).decode('ascii')
image_filename_bot = '[www.cr2.cl][151]header_back.png'
encoded_image_bot = base64.b64encode(open(image_filename_bot, 'rb').read()).decode('ascii')
image_filename_tololo = 'Tololo.png'
encoded_image_tololo = base64.b64encode(open(image_filename_tololo, 'rb').read()).decode('ascii')
drop1_1 = [{'label': 'All', 'value': 'All'}]
drop1_2 = [{'label': str(i), 'value': str(i)} for i in range(1995,2020)]    
drop1_1.extend(drop1_2)
colors = {
    'background': 'white',
    'text': '#7FDBFF',
    'background_2': 'white',
    'background_3': 'cyan'

}
DMC_hourly = completitud(DMC_data, 18, 'D')[0]
EBAS_D = completitud(EBAS_data, 18 ,'D')[0]

# button_layer_1_height = 1.2
# button_layer_2_height = 1.065
# fig1 = go.Figure()
# fig1.add_trace(go.Scatter(x=DMC_data.resample(rule='D').mean().index, 
#                          y=DMC_data.resample(rule='D').mean().O3_ppbv,
#               name="DMC Measurement", mode='markers', 
#               marker={'opacity':0.5, 'size':6
#                       ,
#               'line':{'width': 0.5, 'color': 'white'}})
#               )
              
# fig1.add_trace(go.Scatter(x=EBAS_data.resample(rule='D').mean().index
#                          , y=EBAS_data.resample(rule='D').mean().O3_ppbv,
#               name="EBAS Measurement",mode='markers', 
#               marker={'opacity':0.5, 'size':6,
#               'line':{'width': 0.5, 'color': 'white'}})
#               )

# fig1.update_layout(
#     title="Tololo Time Series",
#     updatemenus=[
#         dict(
#             buttons=list([
#                 dict(
#                     args=[{"x":[DMC_data.resample(rule='H').mean().index,
#                           EBAS_data.resample(rule='H').mean().index],
#                            "y":[DMC_data.resample(rule='H').mean().O3_ppbv,
#                           EBAS_data.resample(rule='H').mean().O3_ppbv]}],
#                     label="Hour",
#                     method="restyle"
#                 ),
#                 dict(
#                     args=[{"x":[DMC_data.resample(rule='D').mean().index,
#                           EBAS_data.resample(rule='D').mean().index],
#                            "y":[DMC_data.resample(rule='D').mean().O3_ppbv,
#                           EBAS_data.resample(rule='D').mean().O3_ppbv]}]
#                     ,
#                     label="Day",
#                     method="restyle"
#                 ),
#                 dict(
#                     args=[{"x":[DMC_data.resample(rule='M').mean().index,
#                           EBAS_data.resample(rule='M').mean().index],
#                            "y":[DMC_data.resample(rule='M').mean().O3_ppbv,
#                           EBAS_data.resample(rule='M').mean().O3_ppbv]}],
#                     label="Month",
#                     method="restyle"
#                 ),
#                 dict(
#                     args=[{"x":[DMC_data.resample(rule='Y').mean().index,
#                           EBAS_data.resample(rule='Y').mean().index],
#                            "y":[DMC_data.resample(rule='Y').mean().O3_ppbv,
#                           EBAS_data.resample(rule='Y').mean().O3_ppbv]}],
#                     label="Year",
#                     method="restyle"
#                 ),
#             ]),
#             type = "buttons",
#             direction="right",
#             pad={"r": 10, "t": 10},
#             showactive=True,
#             x=0,
#             xanchor="left",
#             y=button_layer_1_height,
#             yanchor="top"
#         )],
#     xaxis_title="Date",
#     yaxis_title="O<sub>3</sub> [ppbv]",
#     legend_title="Legend Title",
#     font=dict(
#         size=15
#     ))






# x = ['PM<sub>10</sub>','PM<sub>2.5</sub>',  'O<sub>3</sub>' , 'NO<sub>2</sub>']

# info_con = { 'PM10': 'PM<sub>10</sub> (in \u03bcg/m\u00b3)', 
#              'PM25': 'PM<sub>2.5</sub> (in \u03bcg/m\u00b3)',  
#              'O3': 'O<sub>3</sub> (in ppbv)' , 
#              'NO2': 'NO<sub>2</sub> (in ppbv)' ,              
#              'AOD': 'AOD> (550nm)'}
# ------------------------------App layout------------------------------------
#a = dfold.groupby([dfold.index.month, dfold.index.hour]).mean()
app = dash.Dash(__name__)
app.layout = html.Div([
    html.A([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image_top), 
             style={'height':'10%', 'width':'100%'})
    ], href='http://www.cr2.cl/'), 
    html.Label('Language: '), 
    html.Button('English', id='btn1', n_clicks=0, value='English'),
    dbc.Button('Espanish', id='btn2', n_clicks=0, active=True)
            , html.Div(id='tabs-content'), html.Br(id='Language')]) 
@app.callback(Output('tabs-content', 'children'),
              Output('Language','children'),
              Input('btn1', 'n_clicks'),
              Input('btn2', 'n_clicks'))
def render_content(btn1, btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn1' in changed_id:
        return [html.Div([dcc.Markdown(dedent(f'''
                # **Tololo** (30.169 S, 70.804 W, 81m)
                Principal Investigators: Laura Gallardo, CR2 – Center for Climate and Resilience Research.
                
                Email: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl)
                
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Carmen Vega, DMC - Chilean Meteorological Office
                
                Email : [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
                
                Av. Portales 3450, Estación Central, Chile 
                
                Data Site Manager: Francisca Muñoz, CR2 – Center for Climate and Resilience Research.
                
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).
    
                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                
                
                '''))] ,  
                style={'color': 'black', 'width':'50%','fontFamily': '"Times New Roman"'
                                                    ,'backgroundColor': 'White', 'display': 'inline-block'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'100%', 'width':'100%'})], 
                                    
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%'}),                                                                                  
      html.H1("Trends", style={'text-align': 'center', 'color': '#0668a1','backgroundColor':'white'}),
        html.Div([html.Label('Trends: '),
                  html.Button('Lamsal', id='btn-Lamsal', n_clicks=0),
                  html.Button('Carbone', id='btn-Carbone', n_clicks=0),
                  html.Button('Linear', id='btn-Linear', n_clicks=0)]),
        
        html.Div([dcc.Graph(id='Tendency_graph')]),              
    html.H1("Month-Hour Diagram", style={'text-align': 'center', 'color': '#0668a1','backgroundColor':'white'}),
    html.Div([ html.Label('Date Range:'),
            dcc.DatePickerRange(
                id='calendar_1',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'white'}),
        dcc.Graph(id="grafico2"),
        html.H1("Boxplot", style={'text-align': 'center','color': '#0668a1','backgroundColor':'White'})
        
    ,html.Div([html.Label('Date Range:'),
            dcc.DatePickerRange(
                id='calendar_2',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3),
                )], style={'backgroundColor':'white'})
        
    ,html.Div([html.Label('Period: '),
                  html.Button('Hourly', id='btn_Hourly', n_clicks=0),
                  html.Button('Monthly', id='btn_Monthly', n_clicks=0)])
            ,
    dcc.Graph(id="boxplot1", style={'backgroundColor':'white'}), 
    html.H1("Histogram", style={'text-align': 'center','color': '#0668a1','backgroundColor':'White'}),
    html.Div([html.Label('Date Range:'),
            dcc.DatePickerRange(
                id='calendar_3',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'white'}),
    dcc.Graph(id="histogram", style={'backgroundColor':'white'}),
    html.Div([dcc.Markdown(dedent(f'''CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite L. Gallardo, A. Henríquez, A. M. Thompson, R. Rondanelli, J. Carrasco, A. Orfanoz-Cheuquelaf and P. Velásquez, The first twenty years (1994-2014) of Ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.), Tellus B, 2016. (DOI: 10.3402/tellusb.v68.29484)

View in Tellus'''))]),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image_bot), 
              style={'height':'10%', 'width':'100%'})
], 'English'
    if 'btn2' in changed_id:
       return [html.Div([dcc.Markdown(dedent(f'''
                # **Tololo** (30.169 S, 70.804 W, 81m)
                Principales Investigadoras: Laura Gallardo, CR2 – Centro de Ciencia del Clima y la Resiliencia.
                
                Email: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl)
                
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Carmen Vega, DMC - Dirección Meteorológica de Chile
                
                Email : [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
                
                Av. Portales 3450, Estación Central, Chile
                
                Data Site Manager: Francisca Muñoz, CR2 – Centro de Ciencia del Clima y la Resiliencia.
                
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).
    
                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                '''))] ,  
                style={'color': 'black', 'width':'50%','fontFamily': '"Times New Roman"'
                                                    ,'backgroundColor': 'white', 'display': 'inline-block'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'100%', 'width':'100%'})],
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%'}), 
                html.H1("Linea de Tendencia", style={'text-align': 'center', 'color': '#0668a1','backgroundColor':'white'}),
        html.Div([html.Label('Tendencia: '),
                  html.Button('Lamsal', id='btn-Lamsal', n_clicks=0),
                  html.Button('Carbone', id='btn-Carbone', n_clicks=0),
                  html.Button('Linear', id='btn-Linear', n_clicks=0)]),
        
        html.Div([dcc.Graph(id='Tendency_graph')]),              
    html.H1("Diagrama Mes-Hora", style={'text-align': 'center', 'color': '#0668a1','backgroundColor':'white'}),
    html.Div([ html.Label('Intervalo de tiempo:'),
            dcc.DatePickerRange(
                id='calendar_1',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'white'}),
        dcc.Graph(id="grafico2"),
        html.H1("Diagrama de Cajas y Bigotes", style={'text-align': 'center','color': '#0668a1','backgroundColor':'White'})
        
    ,html.Div([html.Label('Intervalo de tiempo:'),
            dcc.DatePickerRange(
                id='calendar_2',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'white'})
        
    ,html.Div([html.Label('Periodo: '),
                  html.Button('Horario', id='btn_Hourly', n_clicks=0),
                  html.Button('Mensual', id='btn_Monthly', n_clicks=0)])
            ,
    dcc.Graph(id="boxplot1", style={'backgroundColor':'white'}), 
    html.H1("Histograma", style={'text-align': 'center','color': '#0668a1','backgroundColor':'White'}),
    html.Div([html.Label('Intervalo de tiempo:'),
            dcc.DatePickerRange(
                id='calendar_3',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'white'}),
    dcc.Graph(id="histogram", style={'backgroundColor':'white'}),
    html.Div([dcc.Markdown(dedent(f'''CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite L. Gallardo, A. Henríquez, A. M. Thompson, R. Rondanelli, J. Carrasco, A. Orfanoz-Cheuquelaf and P. Velásquez, The first twenty years (1994-2014) of Ozone soundings from Rapa Nui (27°S, 109°W, 51m a.s.l.), Tellus B, 2016. (DOI: 10.3402/tellusb.v68.29484)

View in Tellus'''))]),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image_bot), 
              style={'height':'10%', 'width':'100%'})

                    ], 'Espanish'
            
#     html.Div([dcc.Markdown(dedent(f'''
#             # **Tololo** (30.169 S, 70.804 W, 81m)
#             Principal Investigator: Laura Gallardo, CR2 – Center for Climate and Resilience Research.
            
#             Email: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl)
            
#             Av. Blanco Encalada 2002, Santiago, Chile
            
#             Data Site Manager: Francisca Muñoz, CR2 – Center for Climate and Resilience Research.
            
#             Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
            
#             Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).

#             The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.

#             Contact the station principal investigator(s) for questions concerning data techniques and quality.
            
#     '''))] ,  
#             style={'color': 'black', 'width':'50%','fontFamily': '"Times New Roman"'
#                                                 ,'backgroundColor': 'whitesmoke', 'display': 'inline-block'}) , 
    #                       html.Div([
    # html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
    # style={'height':'100%', 'width':'100%'})]
    # , style={'display': 'inline-block', 'float':'right', 'width': '50%'}),
#     html.H1("Tololo O3 Measurement", style={'text-align': 'center','color': 'white' ,'backgroundColor':'#e2e2e2'}),
#     dcc.Graph(id="grafico1", figure=fig1),
#     html.H1("Month-Hour Diagram", style={'text-align': 'center','backgroundColor':'#e2e2e2'}),
#     html.Div([ html.Label('Date Range:'),
#             dcc.DatePickerRange(
#                 id='calendar_1',
#                 start_date=date(1997, 5, 3),
#                 end_date=date(1998,5,3)
#                 )], style={'backgroundColor':'#e2e2e2'}),
#         dcc.Graph(id="grafico2"),
#         html.H1("Tencency line", style={'text-align': 'center','backgroundColor':'#e2e2e2'}),
#         html.Div([ html.Label('Tendencia: '),
           
#         dcc.RadioItems(
#             id='trend1',
#             options=[
#                 {'label': 'Lamsal', 'value': 'lamsal'},
#                 {'label': 'Carbone', 'value': 'carbone'},
#                 {'label': 'Linear', 'value': 'linear'}
#                 ],
#             value='lamsal',
#             labelStyle={'display': 'inline-block'}
#             )  ]) ,
        
#         html.Div([dcc.Graph(id='Tendency_graph')]),
#     html.H1("Boxplot", style={'text-align': 'center','backgroundColor':'#e2e2e2'}),
#     html.Div([ html.Label('Year(s)): '),
#             dcc.Dropdown(
#                 id='drop_box2',
#                 options=drop1_1,
#                 value='All'
#             )
#         ],
#         style={'width': '20%', 'display': 'inline-block'}),
#     html.Div([
#             dcc.RadioItems(
#                 id='radio1',
#                 options=[{'label':'Horas', 'value':'Horas'},{'label':'Meses', 'value':'Meses'} ],
#                 value='Meses' ,
#                 labelStyle={'display': 'inline-block'} )] ,
#                 style={'display': 'block','backgroundColor':'#e2e2e2'}),
#     dcc.Graph(id="boxplot1", style={'backgroundColor':'#e2e2e2'}), 
#     html.Img(src='data:image/png;base64,{}'.format(encoded_image_bot), 
#               style={'height':'10%', 'width':'100%'})
# ])

@app.callback(
    Output('grafico2', 'figure'),
      [Input('calendar_1', 'start_date'),
      Input('calendar_1', 'end_date'),
      Input('Language', 'children')])
def update_graph(start_date, end_date, Language):
 
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    a = g.groupby([g.index.month, g.index.hour]).mean()
    O3_mesh = [a.O3_ppbv.values[24*i:24*(i+1)] for i in range (0,13)]
    if Language == 'English':
        Months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        xlabel = 'Hour'
        ylabel = 'Month'
    if Language =='Espanish':
        Months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        xlabel = 'Hora'
        ylabel = 'Mes'
    fig = go.Figure(data=(go.Contour(z=O3_mesh,
                                  #x = [i for i in range(24)],
                                  #y = [i for i in range(1,13)])])
                                  x =["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11" , "12", "13", "14", "15", "16", "17", "18", "19", "20", "21","22","23"],
                                  y = Months, colorscale= 'viridis',
                                  
                                  colorbar=dict(
            title='O<sub>3</sub> [ppbv]', # title here
            titleside='right',
            titlefont=dict(
                size=14,
                family='Arial, sans-serif')), contours=dict(
            coloring ='heatmap',
            showlabels = True, # show labels on contours
            labelfont = dict( # label font properties
                size = 13,
                color = 'black')
            ))))

    fig.update_layout(
        width=1200,
        height=500,
        autosize=False,
        margin=dict(t=100, b=0, l=100, r = 100),
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='white',
        paper_bgcolor='white',
        titlefont=dict(size=14,color='black'),
        xaxis_title=xlabel,
        yaxis_title=ylabel)
    

# # Update 3D scene options
#     fig.update_scenes(
#         aspectratio=dict(x=1, y=1, z=0.7),
#         aspectmode="manual"
#         )

# Add drowdowns
# button_layer_1_height = 1.08

    return fig


@app.callback(Output('Tendency_graph', 'figure'),
              Input('btn-Lamsal', 'n_clicks'),
              Input('btn-Carbone', 'n_clicks'),
              Input('btn-Linear', 'n_clicks'),
              Input('Language', 'children'))
def update_graph(btn1, btn2, btn3, Language):
    
    df =  pd.concat([DMC_data,EBAS_data]).resample('D').mean()
    #aux_a , aux_b = info_data('2015-01-01 01','2020-08-09 23',df,'D')

    df_m = df.resample('M').mean()["O3_ppbv"]
    df_m_aux  = df_m.fillna(df_m.mean())
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-Lamsal' in changed_id:
       
        def model(t, coeffs):
            return  (coeffs[0] + coeffs[1]*t + coeffs[2]*np.sin(2*np.pi*t/12) + coeffs[3]*np.cos(2*np.pi*t/12) +
                    coeffs[4]*np.sin(4*np.pi*t/12) + coeffs[5]*np.cos(4*np.pi*t/12) + 
                    coeffs[6]*np.sin(6*np.pi*t/12) + coeffs[7]*np.cos(6*np.pi*t/12) +
                    coeffs[8]*np.sin(8*np.pi*t/12) + coeffs[9]*np.cos(8*np.pi*t/12) +
                    coeffs[10]*np.sin(10*np.pi*t/12) + coeffs[11]*np.cos(10*np.pi*t/12) +
                    coeffs[12]*np.sin(12*np.pi*t/12) + coeffs[13]*np.cos(12*np.pi*t/12) +
                    coeffs[14]*np.sin(14*np.pi*t/12) + coeffs[15]*np.cos(14*np.pi*t/12) +
                    coeffs[15]*np.sin(16*np.pi*t/12) + coeffs[16]*np.cos(16*np.pi*t/12) +
                    coeffs[17]*np.sin(18*np.pi*t/12) + coeffs[18]*np.cos(18*np.pi*t/12) 
        )
    
        def residuals(coeffs, y, t):
            return y - model(t, coeffs)
        
        
        x0 = np.array([1, 1 ,1, 1,1 ,1,1,1,1,1,1,1,1,1,1,1,1,1,1], dtype=float)
    
        t = np.arange(len(df_m_aux))
        x, flag = leastsq(residuals, x0, args=(df_m_aux.values, t))
        model_trend =  model(t, x)    


    elif 'btn-Linear' in changed_id:
 
        def model(t, coeffs):
            return  (coeffs[0] + coeffs[1]*t )
    
        def residuals(coeffs, y, t):
            return y - model(t, coeffs)
        
        
        x0 = np.array([1, 1], dtype=float)
    
        t = np.arange(len(df_m_aux))
        x, flag = leastsq(residuals, x0, args=(df_m_aux.values, t))
        model_trend =  model(t, x)    

    if Language== 'English':
        info = ["Decadal Tendency = " + str(round(x[1]*10*12,1)) + ' +/- xx [ppbv]  <br>Mean= '+ str(round(df["O3_ppbv"].mean(),1)) + " [ppbv]"]
        xlabel = 'Date'
    elif Language == 'Espanish': 
        info = ["Tendencia Decadal= " + str(round(x[1]*10*12,1)) + ' +/- xx [ppbv]  <br>Promedio= '+ str(round(df["O3_ppbv"].mean(),1)) + " [ppbv]"]
        xlabel= 'Fecha'
    fig = go.Figure()  
    fig.add_trace(go.Scatter(
            x=df.index,
            y=df["O3_ppbv"],
            mode='markers',
            #text = aux_a    ,  
            marker={
                'size': 6,
                #'color': aux_b,
                'opacity': 0.5,
                'line': {'width': 0.9, 'color': 'black'}
            }
        ))
    fig.add_trace(go.Scatter( 
                x=df_m.index, 
                y=model_trend,
                mode='markers', 
                marker=dict(size= 6, color='black')
                ))
    fig.add_trace(go.Scatter( 
                x=df_m.index[0:1], 
                y= [df["O3_ppbv"].max()*0.8 , df["O3_ppbv"].max()*0.8] , #df_m[0:1]*2.0
                mode='text', 
                marker=dict(size= 6, color='black'),
                text=info,
                textposition="top right",
                textfont=dict(
                family="Times New Roman",
                size=14,
                color="black")  #
                ))
    fig.update_layout(
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        yaxis=dict(
            range=[0, 60]),
        title_font_color = 'dimgray',
        plot_bgcolor='white',
        paper_bgcolor='white',
        titlefont=dict(size=14,color='black'),
        xaxis_title=xlabel,
        yaxis_title="O<sub>3</sub> [ppbv]")
    return fig



    
@app.callback(
    Output('boxplot1', 'figure'),
      [Input('calendar_2', 'start_date'),
      Input('calendar_2', 'end_date'), 
      Input('btn_Hourly', 'n_clicks'),
      Input('btn_Monthly', 'n_clicks'),
      Input('Language','children')])
def update_graph(start_date, end_date, btn_Hourly, btn_Monthly, Language):
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn_Hourly' in changed_id :           
        mat_h = g.set_index(g.index.hour, append=False).unstack()['O3_ppbv']    
        fig = px.box(mat_h,x=mat_h.index, y=mat_h.values,points=False)
        aux1 = [i for i in range(0,24)]
        aux2 = None
        if Language == 'English':
            xlabel = 'Hour'
        elif Language == 'Espanish':
            xlabel = 'Hora'    
    elif 'btn_Monthly' in changed_id:
        mat_h = g.set_index(g.index.month, append=False).unstack()['O3_ppbv']
        fig = px.box(mat_h, x=mat_h.index, y=mat_h.values, points=False)
        if Language == 'English':
            aux1 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            xlabel = 'Month'
        elif Language == 'Espanish':
            aux1 = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
            xlabel = 'Mes' 
        aux2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 , 12]

    
    fig.update_layout(
    #    autosize=False,
    #    width=500,
    #    height=500,
        #title = zaxis6_name,
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(
            #title_text= '<b>' + yaxis6_name + '</b>', 
        titlefont=dict(size=14,color='black')),
        xaxis=dict(
            #title_text="<b>"+ radio2_name + "</b> ",
            ticktext=aux1,
            tickvals=aux2,
    #        tickmode="array",
        titlefont=dict(size=14,color='black'),
      ),xaxis_title=xlabel,
        yaxis_title="O<sub>3</sub> [ppbv]")
    return fig      

@app.callback(
    Output('histogram', 'figure'),
      [Input('calendar_3', 'start_date'),
      Input('calendar_3', 'end_date'),
      Input('Language','children')])
def update_graph(start_date, end_date, Language):
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    fig = px.histogram(g, x=g.O3_ppbv, histnorm='probability density')
    if Language == 'English':
        ylabel = 'Probability Density'
    if Language == 'Espanish':
        ylabel = 'Probabilidad'
    fig.update_layout(
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='white',
        paper_bgcolor='white',
        titlefont=dict(size=14,color='black'),
        yaxis_title=ylabel,
        xaxis_title="O<sub>3</sub> [ppbv]")    
    return fig
if __name__ == '__main__':
    app.run_server(debug=True, port = 8050)
