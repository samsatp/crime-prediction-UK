# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, html, Input, Output, State, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import random
import json
from VIZ.utils import number_2_color

with open('VIZ\coords.json', 'r') as f:
    coords = json.load(f) 


# Data frame ----
df = pd.read_csv('EDA\df_preprocessed.csv')
lats, longs = [], []

# Find minimum lat, long for work-around colorscale
for _, coord in coords.items():
    lats += [e[0] for e in coord]
    longs += [e[1] for e in coord]

min_coord = [min(lats), min(longs)]


# dummy safty index
nums = [ 
    np.random.random() for _ in coords
]
## its corresponding color
val = [
    number_2_color(r)
    for r in nums
]

# Traces: Main
def get_dummy_fig2():
    traces = [
    {
        "fill": "toself", 
        "line": {
            "color": "rgb(100, 100, 100)", 
            "width": 0.75
        }, 
        "mode": "lines", 
        "type": "scatter", 
        "x": [e[1] for e in coord], 
        "y": [e[0] for e in coord], 
        "fillcolor": val[i], 
        "showlegend": False,
        "hoverlabel": dict(namelength=0),
        "name": force,
        "hovertemplate" : f'<extra></extra>',
        "text": f'<b>{force}</b> <br>Safe-index: {round(nums[i],2)}'
    }
    for i, (force, coord) in enumerate(coords.items())
    ]

    

    data = go.Data(traces)
    layout = {
        "margin": {'l':40, 'r':0, 'b':0, 't':30},
        "width": 600,  
        "height": 700, 
        "hovermode": "closest", 
        "plot_bgcolor": "rgba(0,0,0,0)",
        'xaxis': {'title': '',
                'visible': False,
                'showticklabels': False},
        'yaxis': {'title': '',
                'visible': False,
                'showticklabels': False},
        'legend': {
            'itemclick':'toggle'
        }
    }
    return go.Figure(data=data, layout=layout)

crime_types = ['Violence and sexual offences',
       'Anti-social behaviour', 'Public order', 'Criminal damage and arson',
       'Other theft', 'Vehicle crime', 'Burglary', 'Shoplifting', 'Drugs',
       'Bicycle theft', 'Other crime', 'Robbery', 'Possession of weapons',
       'Theft from the person']

# Trace: Secondary
from typing import Union, List
def get_dummy_secondary(location = 'cheshire', crime_types_selected: Union[str, List[str]] = 'All'):
    temp= df[df['location']==location][['month'] + crime_types]
        
    temp.set_index('month', inplace=True)
    temp = temp.stack().to_frame().reset_index()
    temp.columns = ['month', 'crime type', 'number of crimes']
        
    if crime_types_selected in ['All', ['All']]:
        fig = px.line(
            data_frame=temp,
            x = 'month',
            color='crime type',y='number of crimes',
            template='ggplot2'
            )
    else:
        print('crime_types_selected: ',crime_types_selected)
        fig = px.line(
            data_frame = temp[temp['crime type'].isin(crime_types_selected)],
            x = 'month',
            y='number of crimes',
            color='crime type',
            template='ggplot2'
        )

    fig.update_traces(
        hovertemplate='<i>Number of crimes</i>: <b>%{y:d} cases</b>'+
        '<br>Time: <b>%{x}</b><br>'
    )

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="right",
            x=1,
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        ),
        width = 700,
        height = 700,
        margin={'l':0, 'r':0, 'b':0, 't':30},
        
    )
    return fig

# ----
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server


col1 = dbc.Col(
    html.Div(
        children = [
            html.H2(
                "UK BeSafe Map",
                style={
                    'text-align':'center'
                }
            ),
            html.P(
                '''
                    This is a map showing safe-index predicted by the model developed on past data
                '''
            ),
            dcc.Graph(
            id='main-graph',
            figure=get_dummy_fig2(),
            style={
                'width': '50%',
                'height':'100%',
                'text-align':'center',
                'align-items':'center'
            }
            )
        ],
        style={
            'align-items':'center',
            'text-align':'left',
            "width": "100%","height": "100%",
        }
    ), 
    className='col', id='col1'
    )




col2 = dbc.Col(
    html.Div([
        html.Div([
            dcc.Dropdown(
                    options=
                    [
                        {'label': force, 'value': force}
                        for force in coords.keys()
                    ], 
                    searchable=False, 
                    placeholder="Select the area", 
                    id='location_selector', 
                    clearable=False,
                    value='essex'
                ),
            dcc.Dropdown(
                    options=
                    [
                        {'label': crime_type, 'value': crime_type}
                        for crime_type in crime_types
                    ] + [{'label':'All', 'value':'All'}], 
                    searchable=False, 
                    placeholder="Select the crime type to focus", 
                    id='crime_selector', 
                    clearable=True,
                    value='All',
                    multi=True
                )
            ],
            style={
                'text-align':'center',
                'align-items': 'center',
                'width': 700
            }
        ),
        dcc.Graph(
            figure=get_dummy_secondary(),
            id='secondary'
            ),
        
        ]
    ), 
    className='col', id='col2',
    style={
        'width': '600px',
        'height':'100%'
    }
    )



app.layout = html.Div(children=[
    html.Div(
        [
            html.H1(
            children='Be Safe',
            style={
                'text-align':'center',
                'background-color':'#ABBAEA',
                'padding':'30px'
            }
            ),
            html.P(
            [
            'Mini-project Intro to Data Science', html.Br(),
            'This is the project for predicting safe-index of each area in th UK based on data from Police UK crime database.', 
            ],
            style = {
                'background-color':'#EBEBEB',
                'padding':'20px'
            }
            )
        ]
    )
   ,
   html.Div(
        dbc.Row([
            col1,
            col2    
        ]),
        style={
            'margin':'30px'
        }
   )
])


@app.callback(
    Output('secondary','figure'),
    Input('location_selector', 'value'),
    Input('crime_selector', 'value')
)
def cahnge_location(selected_loc, seleted_crimes):
    print('seleted_crimes: ',seleted_crimes)
    return get_dummy_secondary(location=selected_loc, crime_types_selected=seleted_crimes)
if __name__ == '__main__':
    app.run_server(debug=True)
