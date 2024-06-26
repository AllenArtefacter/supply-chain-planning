import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import os 
import pandas as pd 
from simulation import generate_simulation,get_status,ttl_sales_through_rate,ttl_sales_shortage_rate
from elements import (
    channel_parameter_element,
    legend_description,
    service_range2,
    service_range3,
    service_range4,
    service_range1,
    search_result_aggrid
)

root_path = os.path.dirname(os.path.dirname(__file__))
history_path = os.path.join(root_path, 'data', 'sales_history.csv')
forecast_path = os.path.join(root_path, 'data', 'sales_forecast.csv')
hub_path = os.path.join(root_path, 'data', 'hub_stock.csv')

df_history = pd.read_csv(history_path)
df_forecast = pd.read_csv(forecast_path)
df_hisdf_hub_stocktory = pd.read_csv(hub_path)

app = dash.register_page(__name__)

layout = html.Div(
    [         
    # dcc.Store(id='status'),
    # dcc.Store(id='allocation'),
    # dcc.Store(id='config'),
    # dcc.Store(id='config-records'),
        dcc.Store(id = 'hold-buttom', data = [False]),
        html.Div(
            [
             #'main',
                html.Div(
                    [
                        html.Div('Parameters', style={'margin':'20px','font-size':'30rem'}),
                        html.Div([
                                'select tranportation to hub',
                                dcc.Dropdown(
                                    ['Sea(20 days)', 'Air(10 days)'],
                                    ['Sea(20 days)', 'Air(10 days)'],
                                    id='transportation1',
                                    multi=True, 
                                    searchable=False,
                                    placeholder="Select a transportation method",
                                    persistence=True
                                )
                            ], 
                            style={'margin':'20px'}
                        ),
                        html.Div([
                                'select tranportation to channel',
                                dcc.Dropdown(
                                    ['Trunk(5 days)', 'Air(2 days)'],
                                    ['Trunk(5 days)', 'Air(2 days)'],
                                    id='transportation2',
                                    multi=True, 
                                    searchable=False,
                                    placeholder="Select a transportation method",
                                    persistence=True
                                )
                            ], 
                            style={'margin':'20px'}
                        ),
                        html.Div([
                            'Set channel and sevice level',
                            html.Br(),
                            html.Br(),
                            'channel 1',
                            service_range1,
                            html.Br(),
                            'channel 2',
                            service_range2,
                            html.Br(),
                            'channel 3',
                            service_range3,
                            html.Br(),
                            'channel 4',
                            service_range4
                            ], style={'margin':'20px'}),
                        html.Div(
                            [   
                                dcc.Loading(
                                    [
                                        html.Button('Optimize', id='optimize', n_clicks=0),
                                        html.Div('', id = 'loading-optimize-button')
                                    ],
                                    id = 'loading-button',
                                    type = 'circle'
                                )
                            ], 
                            style={'margin':'20px'}
                        ),
                    ], 
                    style = {'width':'20%','height':'1000px', 'background-color': '#eff2f6ff', 'display': 'inline-block'}
                ),
                html.Div(
                    [
                        html.Div(
                            dcc.Loading(search_result_aggrid(pd.DataFrame()), type="cube"),
                            style={'display': 'inline-block', 'width': "75%",'verticalAlign' : 'bottom'}
                        ),
                        html.Div('',id = 'optimize-display', style = {'display': 'inline-block', 'border':"solid 0px grey", 'border-radius':'2px','width':'24%', 'height':'240px','verticalAlign' : 'bottom'}),
                        html.Div(dcc.Loading(id="test1", type="cube")),
                        html.Div(id="status-details",),
                     
                     ],
                    style = {'width':'80%', 'height':'1000px','background-color':'#f5f7f9','display': 'inline-block','verticalAlign' : 'bottom'}
                )
            ]
        ),
    ]
    ,style = {'height':'1000px', 'background-color':'white', 'margin-top':'0', 'margin-left':'0%', 'margin-right':'0%'}
)



from callbacks import show_staus_from_config