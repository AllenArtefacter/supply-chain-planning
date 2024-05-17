
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
        },
        persistence = True, 
        persisted_props = ['virtualRowData', 'rowData','filterModel','cellValueChanged']
)

def search_result_aggrid(data, id = 'search-results'): 
    columnDefs = [
         {'field': 'trial','cellStyle': {'font-size': '12rem'}, 'maxWidth':100, "checkboxSelection": True},
         {'field': 'sales through','cellStyle': {'font-size': '12rem'}, 'maxWidth':100,
          'valueFormatter': {"function":"params.value == null ? '' :  d3.format(',.1%')(params.value)" }},
         {'field': 'fill rate','cellStyle': {'font-size': '12rem'}, 'maxWidth':100,
          'valueFormatter': {"function":"params.value == null ? '' :  d3.format(',.1%')(params.value)" }},
         {'field': 'transportation days (to hub)','cellStyle': {'font-size': '12rem'}, 'maxWidth':100,},
         {'field': 'transportation days (to channel)','cellStyle': {'font-size': '12rem'}, 'maxWidth':150,},
         {'field': 'service level and order','cellStyle': {'font-size': '12rem'}, 'maxWidth':400,},
     ]

    agid = dag.AgGrid(
            id=id,
            rowData= data.to_dict('records'),
            columnDefs=columnDefs,
            # defaultColDef={"filter": False},
            columnSize="sizeToFit",
            dashGridOptions={"rowSelection":"single", "rowDragManaged": True, "rowDragEntireRow": True,},
            style= {
                'height':240, 'font-size':'12rem', 'text-flow':'clip'
            }
    )
    
    return [agid]
    
    

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
        html.Div(style = {'display': 'inline-block', 'width': '20px', 'height': '20px', 'background-color': '#577B8D','margin-left':'20px'}),
        html.Div('Stockout',style = {'display': 'inline-block','verticalAlign':'middle', 'width': '120px', 'height': '20px','margin-left':'10px','margin-bottom':'10px'}),
        
    ],
    style = {'height': '30px', 'border':'solid 0px grey','border-radius':'2px'}
)



def service_level(id):
    range_slider = dcc.RangeSlider(
        id = id,
        min=60,
        max=100,
        step=10,
        marks={
            60: '60',
            70: '70',
            80: '80', 
            90: '90',
            100: '100', 
        },
        value=[60, 70],
        persistence = True,
    )
    
    return html.Div(range_slider, style = {'margin-left':'50px','width':'200px'})


service_range1 = service_level('channel1-service-level')
service_range2 = service_level('channel2-service-level')
service_range3 = service_level('channel3-service-level')
service_range4 = service_level('channel4-service-level')