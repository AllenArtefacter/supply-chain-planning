# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash
import plotly.express as px
import pandas as pd
import base64
import os 
import dash_ag_grid as dag
import dash_auth
import sys 
sys.path.insert(0, os.path.dirname(__file__))

import callbacks
import simulation
import elements

logo_path = os.path.join(os.path.dirname(__file__), 'assets', '220px-Estée_Lauder_Companies_logo.svg.png')
logo = base64.b64encode(open(logo_path, 'rb').read()).decode('ascii')
logo_black_path = os.path.join(os.path.dirname(__file__), 'assets', 'Artefact-AI-is-about-People.png')
logo_black = base64.b64encode(open(logo_black_path, 'rb').read()).decode('ascii')

VALID_USERNAME_PASSWORD_PAIRS = {
    'artefact': 'artefact'
}

app = Dash(__name__, use_pages=True)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.config.suppress_callback_exceptions = True
# app.css.config.serve_locally = True
app.layout = html.Div([
    dcc.Store(id='status'),
    dcc.Store(id='allocation'),
    dcc.Store(id='config-records', data = []),
    dcc.Store(id='config-records-list', data = []),
    dcc.Store(id='config-search-records', data = []),
    dcc.Store(id='config'),
    dcc.Download(id = 'download'),
    dcc.Location(id='url'),
    html.Div(
        [
            html.Img(src='data:image/png;base64,{}'.format(logo),style = {'verticalAlign' : 'top', 'margin':'20px' ,'height': '50px', 'display': 'inline-block'}),
            #html.Div('留个横幅',style= {'verticalAlign' : 'bottom', 'font-size':10,'width': '60%','display': 'inline-block'}),
            html.Div(
                [
                    html.Div(dcc.Link(f"Planner", href="/planner",style = {'text-decoration':'none'}), style = {'display': 'inline-block', 'margin-top':'0px','margin-left':'0px', 'verticalAlign':'bottom','margin-right':'30px'}),
                    html.Div(dcc.Link(f"Optimizer", href="/optimizer",style = {'text-decoration':'none'}),style = {'display': 'inline-block','margin-left':'30px', 'verticalAlign':'bottom','margin-right':'30px'}),
                    html.Div(dcc.Link(f"Alert", href="/alert",style = {'text-decoration':'none'}),style = {'display': 'inline-block','margin-left':'30px', 'verticalAlign':'bottom','margin-right':'30px'})
                ],
                style = {'margin-left':'15%', 'margin-right':'30%','verticalAlign':'bottom', 'display': 'inline-block'}
            )
        ],style = dict(margin='auto',backgroundImage='linear-gradient(#FFFFFF 20% ,#f4f4f2 80%)',
                             height = '100px',boxShadow='0px 5px 20px 0px #bbbfca',z_index = 999, position = 'relative')
    ),
    html.Div(dash.page_container,style = {'background-color':'white', 'width':'100%'}),
    html.Div(
        [
            html.Img(src='data:image/png;base64,{}'.format(logo_black),style = {'margin-top':'50px','verticalAlign' : 'bottom', 'width': '10%', 'display': 'inline-block'}),
        ]
    ,style = {'height':'400px','width':'100%', 'background-color':'#0a1128ff'})
])

if __name__ == '__main__':
    app.run(debug=True, port = '9091')