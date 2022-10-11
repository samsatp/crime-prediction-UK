# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, html, dcc
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

    ## Last trace as a worksround to make Plotly show colorscale
    traces.append({
    "mode": "markers", 
    "fill": "toself",
    "name": "", 
    "type": "scatter", 
    "x": [min_coord[1]], 
    "y": [min_coord[0]], 
    "line": {
        "width": 0.75
    },
    "marker": {
        "color": "rgb(100, 100, 100)",
        "size": 0, 
        "colorbar": {
        "thickness": 20
        }, 
        "colorscale": [
        [0.0, "red"], [1.0, "green"]
        ],
        "cmin":0,"cmax":1
    }, 
    "showlegend": False
    } )

    data = go.Data(traces)
    layout = {
    "title": "UK Choropleth Map", 
    "width": 750,  
    "height": 950, 
    "hovermode": "closest", 
    "plot_bgcolor": "rgba(0,0,0,0)"
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
        color='crime type',y='number of crimes'
        )
    return fig

# ----
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

def get_dummy_fig():
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color="country", title="some plots of that area")
    return fig

def get_fig():
    fig = go.Figure()
    for force, coord in coords.items():
        lat, lon = [e[0] for e in coord], [e[1] for e in coord]
        fig.add_trace(
            go.Scattermapbox(
                lat=lat, lon=lon,
                fill = "toself",
                mode = "lines",
                marker = { 'size': 10, 'color': "orange" },
                name=force,
                hovertemplate = f'''
                    <b>Area: {force}</b><br>
                    <b>safe-index: {round(random.random(), 2)}</b>
                    <extra></extra>''',
                showlegend = False,
                hoverinfo='none'
            ),
            
        )

    fig.update_layout(
        margin = {'l':0, 'r':0, 'b':0, 't':0},
        mapbox = {
            'style': "open-street-map",
            'center': {'lat': 52.8739609957, 'lon': -3.464840987388 },
            'zoom': 5},
        showlegend = False)

    return fig


col1 = dbc.Col(
    html.Div(
        children = dcc.Graph(
        id='example-graph',
        figure=get_dummy_fig2(),
        style={
            'width': '500px',
            'height':'500px',
            'text-align':'center',
            'align-items':'center'
        }
        ),
        style={
            'align-items':'center',
            'text-align':'center',
            "width": "100%","height": "100%",
        }
    ), 
    className='col', id='col1'
    )




col2 = dbc.Col([
    html.Div([
        html.Div([
            dcc.Dropdown(options=
                [
                    {'label': force, 'value': force}
                    for force in coords.keys()
                ], searchable=False, placeholder="Select the area", id='model_selection', clearable=False),
            ])
        ],
        style={
            'text-align':'center',
            'align-items': 'center',
        }, 
    ),
    html.Div(
        dcc.Graph(
            figure=get_dummy_secondary()
        )
    )], 
    className='col', id='col2'
    )

app.layout = html.Div(children=[
    html.H1(
        children='Be Safe',
        style={
            'text-align':'center'
        }
    ),

    html.Div(
        children='Mini-project Intro to Data Science',
        style = {
            'text-align':'center',
            'margin' : '30px'
        }
    ),
    
    dbc.Row([
        col1,
        col2    
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
