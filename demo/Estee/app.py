# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash
import plotly.express as px
import pandas as pd
import base64
import os 
import dash_ag_grid as dag

logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'Artefact-AI-is-about-People-Blue-scaled.png')
logo = base64.b64encode(open(logo_path, 'rb').read()).decode('ascii')
logo_black_path = os.path.join(os.path.dirname(__file__), 'assets', 'Artefact-AI-is-about-People.png')
logo_black = base64.b64encode(open(logo_black_path, 'rb').read()).decode('ascii')


app = Dash(__name__, use_pages=True)
app.config.suppress_callback_exceptions = True
# app.css.config.serve_locally = True
app.layout = html.Div([
    html.Div(
        [
            html.Img(src='data:image/png;base64,{}'.format(logo),style = {'verticalAlign' : 'top', 'height': '30px', 'display': 'inline-block'}),
            html.Div('留个横幅',style= {'verticalAlign' : 'bottom', 'font-size':10,'width': '60%','display': 'inline-block'}),
            html.Div(
                [
                    html.Div(dcc.Link(f"Planner", href="/planner",style = {'text-decoration':'none'}), style = {'display': 'inline-block', 'margin-left':'0px', 'margin-right':'30px'}),
                    html.Div(dcc.Link(f"Optimizer", href="/optimzier",style = {'text-decoration':'none'}),style = {'display': 'inline-block','margin-left':'30px', 'margin-right':'30px'}),
                    html.Div(dcc.Link(f"Alert", href="/alert",style = {'text-decoration':'none'}),style = {'display': 'inline-block','margin-left':'30px', 'margin-right':'30px'})
                ],
                style = {'margin-left':'15%', 'margin-right':'30%','verticalAlign':'bottom', }
            )
        ],style = dict(margin='auto',backgroundImage='linear-gradient(#FFFFFF 20% ,#f4f4f2 80%)',
                             height = '50px',boxShadow='0px 5px 20px 0px #bbbfca',z_index = 999, position = 'relative')
    ),
    html.Div(dash.page_container,style = {'background-color':'white', 'width':'100%'}),
    html.Div(
        [
            html.Img(src='data:image/png;base64,{}'.format(logo_black),style = {'margin-top':'50px','verticalAlign' : 'bottom', 'width': '10%', 'display': 'inline-block'}),
        ]
    ,style = {'height':'200px','width':'100%', 'background-color':'#0a1128ff'})
])

if __name__ == '__main__':
    app.run(debug=True)