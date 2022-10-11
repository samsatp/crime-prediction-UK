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
from utils import number_2_color

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
    "name": force,
    "hovertemplate" : f'Area: {force} <extra></extra><br>Safe-index: {nums[i]}',
    "text": f'Area: {force}<br>Safe-index: {round(nums[i],2)}'
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
                        'showticklabels': False}
    }
    return go.Figure(data=data, layout=layout)


# Trace: Secondary
def get_dummy_secondary(location = 'cheshire'):
    temp= df[df['location']==location][['month', 'Violence and sexual offences',
       'Anti-social behaviour', 'Public order', 'Criminal damage and arson',
       'Other theft', 'Vehicle crime', 'Burglary', 'Shoplifting', 'Drugs',
       'Bicycle theft', 'Other crime', 'Robbery', 'Possession of weapons',
       'Theft from the person']]
        
    temp.set_index('month', inplace=True)
    temp = temp.stack().to_frame().reset_index()
    temp.columns = ['month', 'crime type', 'number of crimes']
    fig = px.line(
        data_frame=temp,
        x = 'month',
        color='crime type',y='number of crimes',
        template='ggplot2'
        )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-1.02,
            xanchor="right",
            x=1
        ),
        width = 700,
        height = 600,
        margin={'l':0, 'r':0, 'b':0, 't':30},
        xaxis = dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    return fig

# ----
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])



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
            id='example-graph',
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
        html.Div(
            dcc.Dropdown(
                    options=
                    [
                        {'label': force, 'value': force}
                        for force in coords.keys()
                    ], 
                    searchable=False, 
                    placeholder="Select the area", 
                    id='location_selector', 
                    clearable=False
                ),
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
    Input('location_selector', 'value')
)
def cahnge_location(selected_loc):
    return get_dummy_secondary(location=selected_loc)
if __name__ == '__main__':
    app.run_server(debug=True)
