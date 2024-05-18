import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import os 
import pandas as pd 
from simulation import generate_simulation,get_status,ttl_sales_through_rate,ttl_sales_shortage_rate
from elements import channel_parameter_element,legend_description,search_result_aggrid




root_path = os.path.dirname(os.path.dirname(__file__))
history_path = os.path.join(root_path, 'data', 'sales_history.csv')
forecast_path = os.path.join(root_path, 'data', 'sales_forecast.csv')
hub_path = os.path.join(root_path, 'data', 'hub_stock.csv')

excel_path = os.path.join(root_path, 'data', 'allocation.xlsx')

df_history = pd.read_csv(history_path)
df_forecast = pd.read_csv(forecast_path)
df_hisdf_hub_stocktory = pd.read_csv(hub_path)

app = dash.register_page(__name__)

layout = html.Div(
    [         
    # dcc.Store(id='status'),
    # dcc.Store(id='allocation'),
    # dcc.Store(id='config-records', data = []),
    # dcc.Store(id='config-records-list', data = []),
    # dcc.Store(id='config'),
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
                                    value = 'Air(10 days)',
                                    id='transportation1', 
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
                                    value = 'Trunk(5 days)',
                                    id='transportation2', 
                                    searchable=False,
                                    placeholder="Select a transportation method",
                                    persistence=True
                                )
                            ], 
                            style={'margin':'20px'}
                        ),
                        html.Div([
                            'Set channel priority and sevice level',
                            channel_parameter_element,
                            html.Div(id="channel-parameter-display")
                            ], style={'margin':'20px'}),
                        html.Div([html.Button('Submit', id='submit1', n_clicks=0)], style={'margin':'20px'}),
                    ], 
                    style = {'width':'20%','height':'950px', 'background-color': '#eff2f6ff', 'display': 'inline-block'}
                ),
                html.Div(
                    [
                        html.Div(search_result_aggrid(pd.DataFrame(), id = 'history')),
                        html.Div(dcc.Loading(id="test4", type="cube")),
                        html.Div(id="test1", hidden=True),
                    ],
                    style = {'width':'80%', 'height':'950px','background-color':'#eff2f6a5','display': 'inline-block','verticalAlign' : 'bottom'}
                )
            ]
        ),
    ]
    ,style = {'height':'950px', 'background-color':'white', 'margin-top':'0', 'margin-left':'0%', 'margin-right':'0%'}
)



from callbacks import (
    get_status_from_prameter,
    display_status_details,
    display_channel_parameter_element
)