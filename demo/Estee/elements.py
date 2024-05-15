
import dash_ag_grid as dag

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