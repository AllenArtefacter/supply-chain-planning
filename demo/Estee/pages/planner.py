import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import os 
from flask_caching import Cache
import pandas as pd 
from simulation import generate_simulation,get_status,ttl_sales_through_rate,ttl_sales_shortage_rate
from elements import channel_parameter_element




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
        html.Div(
            [
                dcc.Store(id='status'),
                dcc.Store(id='allocation'),
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
                                    placeholder="Select a transportation method"
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
                                    placeholder="Select a transportation method"
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
                    style = {'width':'20%','height':'800px', 'background-color': '#eff2f6ff', 'display': 'inline-block'}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(id ='sales-through', style = {'display': 'inline-block', 'width': '100px'}),
                                html.Div(id ='stockout', style = {'display': 'inline-block', 'width': '100px'}),
                            ],
                        style = {'height': '100px'}),
                        html.Div(dcc.Loading(id="test1", type="cube")),
                        html.Div(id="status-details"),
                     
                     ],
                    style = {'width':'80%', 'height':'800px','background-color':'#eff2f6a5','display': 'inline-block','verticalAlign' : 'bottom'}
                )
            ]
        ),
    ]
    ,style = {'height':'800px', 'background-color':'white', 'margin-top':'0', 'margin-left':'15%', 'margin-right':'15%'}
)



from callbacks import * 