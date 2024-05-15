import dash
from dash import html, dcc, callback, Input, Output
import os 

root_path = os.path.dirname(os.path.dirname(__file__))

history_path = os.path.join(root_path, 'data', 'sales_history.csv')
forecast_path = os.path.join(root_path, 'data', 'sales_forecast.csv')
hub_path = os.path.join(root_path, 'data', 'hub_stock.csv')



dash.register_page(__name__)

layout = html.Div([
    html.H1('This is our optimizer page'),
    html.Div([history_path,forecast_path,hub_path])
])






def show_status():
    
    
    return 