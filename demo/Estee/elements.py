
import dash_ag_grid as dag
from dash import html, dcc, callback, Input, Output

channel_parameter_element = dag.AgGrid(
        id='channel-parameter',
        rowData=[
            {'channel name': 'channel 1', 'service level': 80},
            {'channel name': 'channel 2', 'service level': 80},
            {'channel name': 'channel 3', 'service level': 80},
            {'channel name': 'channel 4', 'service level': 80},
        ],
        columnDefs=[
            {'field': 'channel name', 'rowDrag': True,'cellStyle': {'font-size': '12rem'},"wrapText":True, "autoHeight":True},
            {'field': 'service level', 'editable':True, 'cellStyle': {'font-size': '12rem'},"width": 150,"wrapText":True,"autoHeight":True},
        ],
        defaultColDef={"filter": False},
        columnSize="sizeToFit",
        dashGridOptions={"rowDragManaged": True},
        style= {
            'height':240, 'font-size':'12rem', 'text-flow':'clip'
        }
)


legend_description = html.Div(
    [
        html.Div(style = {'display': 'inline-block', 'width': '20px', 'height': '20px', 'background-color': '#98D8AA','margin-left':'20px'}),
        html.Div('Full Stock',style = {'display': 'inline-block','verticalAlign':'middle', 'width': '120px', 'height': '20px','margin-left':'5px','margin-bottom':'10px'}),
        html.Div(style = {'display': 'inline-block', 'width': '20px', 'height': '20px', 'background-color': '#F7D060','margin-left':'20px'}),
        html.Div('Replenishment',style = {'display': 'inline-block','verticalAlign':'middle', 'width': '120px', 'height': '20px','margin-left':'5px','margin-bottom':'10px'}),
        html.Div(style = {'display': 'inline-block', 'width': '20px', 'height': '20px', 'background-color': '#E99497','margin-left':'20px'}),
        html.Div('Risk(Safety Stock)',style = {'display': 'inline-block','verticalAlign':'middle', 'width': '120px', 'height': '20px','margin-left':'5px','margin-bottom':'10px'}),
        html.Div(style = {'display': 'inline-block', 'width': '20px', 'height': '20px', 'background-color': '#FF6363','margin-left':'20px'}),
        html.Div('Near Stockout',style = {'display': 'inline-block','verticalAlign':'middle', 'width': '120px', 'height': '20px','margin-left':'5px','margin-bottom':'10px'}),
        html.Div(style = {'display': 'inline-block', 'width': '20px', 'height': '20px', 'background-color': '#FF6363','margin-left':'20px'}),
        html.Div('Stockout',style = {'display': 'inline-block','verticalAlign':'middle', 'width': '120px', 'height': '20px','margin-left':'10px','margin-bottom':'10px'}),
        
    ],
    style = {'height': '50px', 'border':'solid 0px grey','border-radius':'2px'}
)