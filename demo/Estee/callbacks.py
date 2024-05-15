from dash import Dash, html, dcc, Input, Output, State, callback
import pandas as pd 
import re
import os 
from datetime import datetime as dt 
import dash_ag_grid as dag
import json
import plotly.graph_objects as go 
from datetime import timedelta
import numpy as np 

from simulation import generate_simulation,get_status,ttl_sales_through_rate,ttl_sales_shortage_rate,summarize_status

root_path = os.path.dirname(__file__)
history_path = os.path.join(root_path, 'data', 'sales_history.csv')
forecast_path = os.path.join(root_path, 'data', 'sales_forecast.csv')
hub_path = os.path.join(root_path, 'data', 'hub_stock.csv')

df_history = pd.read_csv(history_path)
df_forecast = pd.read_csv(forecast_path)
df_hub_stock = pd.read_csv(hub_path)

@callback(
    Output("channel-parameter-display", "children"),
    Input("channel-parameter", "virtualRowData"),
)
def display_channel_parameter_element(rows):
    dff = pd.DataFrame(rows)
    # return str(dff.columns)
    
    order = dff['channel name'].tolist()
    
    return 'select order: '+' > '.join(order)


# @callback(
#     Output("test1", "children"),
#     Input("channel-parameter", "virtualRowData"),
#     # State("channel-parameter", "virtualRowData"),
# )
# def call_channel_parameter_element(rows):
#     dff = pd.DataFrame(rows)
    
#     return str(dff)


@callback(
    [Output("test1", "children"),
     Output("status", "data"),
     Output("allocation", "data"),
     Output('sales-through', 'children'),
     Output('stockout', 'children'),
     ],
    Input('submit1', 'n_clicks'),
    State("transportation1", "value"),
    State("transportation2", "value"),
    State("channel-parameter", "virtualRowData"),
    # prevent_initial_call=True
)
def get_status_from_prameter(_, t1,  t2, channel_rows):
    if not t1:
        return "please select tranportation to hub"
    if not t2:
        return "please select tranportation to channel"
    

        
    t1 = float(re.findall(r'\d+', str(t1))[0])
    t2 = float(re.findall(r'\d+', str(t2))[0])
    
    df_channels = pd.DataFrame(channel_rows)
    
    df_channels['service_level'] = df_channels['service level']/100
    df_channels['priority'] = range(len(df_channels))

    channel_dict = df_channels.set_index('channel name')[['priority', 'service_level']].T.to_dict()
    
    config = {
        "lead_time_hud2channel": t2,
        "lead_time_plant2hub": t1,
        "safety_stock_factor" : {
            "A" : 10,
            "B" : 10, 
            "C": 10
        },
        "channel_plan":channel_dict
    }
    # return str(config)
    sku_ls = ['A', 'B', 'C']
    
    df_allocation = generate_simulation(
        config, 
        sku_ls,'2023-01-14', '2023-01-15', df_history, df_forecast, df_hub_stock, [1,2,3,4]
    )
    #df_allocation['date'] = df_allocation['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    sales_through_rate = ttl_sales_through_rate(df_allocation)
    stockout_rate = ttl_sales_shortage_rate(df_allocation)
    df_status = summarize_status(df_allocation)
    
    df_status_ = df_status.copy()
    df_status_.columns = [i.strftime("%Y-%m-%d") if isinstance(i, dt) else i for i in df_status.columns]
    
    status_table = _status2table(df_status)
    
    return (
        status_table, 
        df_status_.reset_index().to_dict('records'), 
        df_allocation.to_dict('records'), 
        f'Total Sales Through: {np.round(sales_through_rate,2)}%',
        f'Stockout Rate: {np.round(stockout_rate,2)}%',
    )

@callback(
    Output("status-details", "children"),
    Input("status-table", "cellClicked"),
    State("status", "data"),
    State("allocation", "data"),
    prevent_initial_call=True
)
def display_status_details(cell, status_records, allocation_records):
    
    df_status = pd.DataFrame(status_records)
    
    
    df_allocation = pd.DataFrame(allocation_records)
    r_idx = cell['rowIndex']
    c_idx = cell['colId']
    c_idx = dt.strptime(c_idx, '%Y %b %d').strftime('%Y-%m-%d') if len(c_idx) ==11 and len(c_idx.split(' '))==3 else None
    
    
    sku, channel  = df_status[['sku_name', 'channel']].values[r_idx]
    
    fig = _plot_details(df_allocation, sku, channel,c_idx)

    return html.Div(
        dcc.Graph(figure=fig,style = {'height':'190px', 'margin':'5px'}),
        style = {'heigh':'200px','margin-top':'1px', 'border':'solid 0.5px grey','border-radius':'2px'}
    )



def _status2table(df_status):
    df_status_ = df_status.reset_index()
    # df_status_['sales_through'] = df_status_['sales_through'].apply('')
    df_status_ = df_status_.rename(columns = {'sku_name':'sku', 'sales_through':'sales through', 'stockout': 'stockout rate'})
    
    datetime_cols = [i.strftime("%Y %b %d") for i in df_status_.columns[4:]]
    df_status_.columns = list(df_status_.columns[:4]) + datetime_cols

    # columnDef = [
    #     {
    #         'headerName': 'Info',
    #         'children':[]
    #     },
    #     {
    #         'headerName': 'Date',
    #         'children':[]
    #     }
    # ]
    
    comment_columnDef = [
        {'field': 'sku','cellStyle': {'font-size': '12xrem'}, 'maxWidth':80,},
        {'field': 'channel','cellStyle': {'font-size': '12rem'}, 'maxWidth':120},
        {'field': 'sales through','cellStyle': {'font-size': '12rem'}, 'valueFormatter': {"function":"params.value == null ? '' :  d3.format(',.1%')(params.value)" }},
        {'field': 'stockout rate','cellStyle': {'font-size': '12rem'}, 'valueFormatter': {"function":"params.value == null ? '' :  d3.format(',.1%')(params.value)" }},
    ]
    
    date_columnDef =  [
        {'field': c, 'cellStyle': {'font-size': '12rem'},'maxWidth':60,'sortable':False,
            'cellStyle': {
            "styleConditions": [
                {
                    "condition": "params.value == 'full'",
                    "style": {"backgroundColor": "#98D8AA", "color":"#98D8AA"},
                },
                {
                    "condition": "['hub', 'manufacture'].includes(params.value)",
                    "style": {"backgroundColor": "#F7D060", "color":"#F7D060"},
                },
                {
                    "condition": "params.value == 'risk'",
                    "style": {"backgroundColor": "#E99497", "color":"#E99497"},
                },
                {
                    "condition": "params.value == 'near stockout'",
                    "style": {"backgroundColor": "#FF6363", "color":"#FF6363"},
                },
                {
                    "condition": "params.value == 'stockout'",
                    "style": {"backgroundColor": "#577B8D", "color":"#577B8D"},
                },
            ]
            
            }
            }
        for c in df_status_.columns[4:]
    ]
    columnDef = comment_columnDef + date_columnDef
    status_table = dag.AgGrid(
            # className= 'ag-status-table',
            id='status-table',
            rowData=df_status_.to_dict('records'),
            columnDefs=columnDef,
            defaultColDef={"filter": False},
            columnSize="sizeToFit",
            columnSizeOptions={
                'defaultMinWidth': 80,
                'columnLimits': [{'key': c, 'minWidth': 50} for c in datetime_cols],
            },
            style= {
                'height':500, 'font-size':'12rem', 'font-family':'Century Gothic', 'margin-top':'0px'
            }
    )
    
    return status_table


def _plot_details(df_allocation,sku, channel, date_id=None):
    fig = go.Figure()
    df_allocation_selected = df_allocation.query(f"sku_name == '{sku}' & channel == '{channel}'")
    df_allocation_selected
    fig.add_hline(y = df_allocation_selected['safety_stock'].values[0], line = dict(color = '#E99497', width = 1, dash = 'dot'))
    fig.add_trace(
        go.Waterfall(
        name = "20", orientation = "v",
        x = df_allocation_selected['date'],
        textposition = "outside",
        # text = df_allocation_selected['status'],
        # decreasing = {"marker":{"color":"#F7D060"}},
        increasing = {"marker":{"color":"#F7D060"}},
        y = [df_allocation_selected['stock'].values[0]] + df_allocation_selected['stock'].diff().tolist()[1:],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.add_annotation(
        x = 1, y = df_allocation_selected['safety_stock'].values[0],
        xref='paper', yref='y',
        xanchor='left',
        align='left',
        text= 'Safety<br>Stock<br>Level',
        showarrow=False,
        font = {'color': '#E99497'}
    )

    max_stock = df_allocation_selected['stock'].max()
    for i, d in df_allocation_selected.reset_index().iterrows():
        if d['status'] not in ['risk', 'full', 'near stockout'] or i == 0:
            fig.add_annotation(
                x = d['date'], y = d['stock'] + max_stock*0.02,
                # xanchor='',
                align='center',
                text= 'current<br>stock'if i==0 else d['status'],
                font = dict(color = 'red' if d['status'] == 'stockout' else 'black'),
                showarrow=True,arrowhead = 2
            )

    fig.update_layout(
        template = 'simple_white',showlegend = False, margin = {'t':30, 'l':0,'b':0, 'r':50},
        font = dict(size = 11, family = 'Century Gothic'), title = f'{sku} {channel}'
    )
    fig.update_xaxes(mirror = True,)
    fig.update_yaxes(mirror = True, title = 'stock', range = [0, max_stock * 1.5])

    if date_id:
        x0 = dt.strptime(date_id, '%Y-%m-%d') - timedelta(days = 0.5)
        x1 = dt.strptime(date_id, '%Y-%m-%d') + timedelta(days = 0.5)
        fig.add_shape(type="rect",
            x0=x0, y0=0, x1=x1, y1=max_stock * 1.5,
            line=dict(
                color="RoyalBlue",
                width=2,
            ),
            fillcolor="LightSkyBlue",
        )

    return fig