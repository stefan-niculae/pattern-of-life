from datetime import datetime
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from graph_generation import generate_graph
from utils import latlon2mgrs, mgrs2latlon


""" Setup """
app = dash.Dash(__name__)
app.title = 'Pattern of Life'
server = app.server


""" Data """
city_coords = {
    'Kabul':            (34.32, 69.10),
    'Kandahar':         (31.37, 65.43),
    'Mazar-e Sharif':   (36.42, 67.07),
    'Herat':            (34.20, 62.12),
    'Jalalabad':        (34.26, 70.26),
    'Kunduz':           (36.43, 68.52),
    'Ghazni':           (33.32, 68.25),
}

entries = pd.read_csv('entries.csv')


""" Layout """
traces, layout = generate_graph(entries)  # initial graph

# TODO make these dynamic as well
civilians_counts = entries.counts[~entries.armed]
civilians_range  = min(civilians_counts), max(civilians_counts)
hostiles_counts  = entries.counts[entries.armed]
hostiles_range   = min(hostiles_counts), max(hostiles_counts)

default_day = 2
default_hour = 15


app.layout = html.Div(id='main-container', children=[
    html.Div(id='left-panel', children=[
        html.H1('Expected Activity'),


        html.H2('Location'),

        html.P('Area:', className='control-label'),
        dcc.Dropdown(
            id='area-dropdown',
            options=[dict(label=city, value=city) for city in city_coords.keys()],
            value='Kabul',
        ),

        html.P('MGRS coordinates:', className='control-label'),
        dcc.Input(
            id='mgrs-input',
            placeholder='example: 42SWC0920097642',
            type='text',
            value='',
        ),
        # dcc.Input(
        #     id='lon-input',
        #     className='coord-input',
        #     placeholder='Longitude',
        #     type='number',
        #     value='69.10'
        # ),


        html.H2('Time'),

        html.P('Day of week:', className='control-label'),
        dcc.Slider(
            id='day-slider',
            min=0, max=6, step=1,
            value=default_day,
            marks=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        ),

        html.P('Hour of day:', className='control-label'),
        dcc.Slider(
            id='hour-slider',
            min=0, max=23, step=1,
            value=default_hour,
            marks={i: i for i in list(range(0, 24, 3)) + [23]},
        ),

        html.Button('Set current day & hour', id='now-button'),


        html.H2('Show'),

        html.P('Data points:', className='control-label'),
        dcc.RadioItems(
            id='show-radio',
            options=[
                dict(label='Hostiles only', value='hostiles'),
                dict(label='Civilians only', value='civilians'),
                dict(label='All', value='all'),
            ],
            value='all',
        ),

        html.P('Map overlay:', className='control-label'),
        dcc.Dropdown(
            id='overlay-dropdown',
            options=[
                dict(label='Simple', value='light'),
                dict(label='Terrain', value='outdoors'),
                dict(label='Satellite', value='satellite-streets'),
            ],
            value='light',
            clearable=False,
            searchable=False,
        ),
    ]),

    html.Div(id='map-container', children=[
        dcc.Graph(
            id='map-chart',
            figure=dict(data=traces, layout=layout),
            config=dict(displaylogo=False),
        )
    ]),

    html.Div(id='legend', children=[
        html.Div(className='colorscale-container', children=[
            html.Div('Civilians', className='colorscale-label', id='civilians-label'),
            html.Div(className='colorscale', id='civilians-colorscale', children=[
                html.Div(className='colorscale-ticks', children=[
                    html.P(civilians_range[0], className='left-tick'),
                    html.P(sum(civilians_range) // 2, className='center-tick'),
                    html.P(civilians_range[1], className='right-tick'),
                ])
            ]),
        ]),
        html.Div(className='colorscale-container', children=[
            html.Div('Hostiles', className='colorscale-label', id='hostiles-label'),
            html.Div(className='colorscale', id='hostiles-colorscale', children=[
                html.Div(className='colorscale-ticks', children=[
                    html.P(hostiles_range[0], className='left-tick'),
                    html.P(sum(hostiles_range) // 2, className='center-tick'),
                    html.P(hostiles_range[1], className='right-tick'),
                ])
            ]),
        ]),
    ]),

])


""" Interactivity """
@app.callback(
    Output('mgrs-input', 'value'),
    [Input('area-dropdown', 'value')]
)
def set_coords_from_area(area_name):
    return latlon2mgrs(city_coords[area_name])

# TODO when setting MGRS coords manually, blank out area dropdown


@app.callback(
    Output('map-chart', 'figure'),
    [
        Input('day-slider', 'value'),
        Input('hour-slider', 'value'),
        Input('show-radio', 'value'),
        Input('mgrs-input', 'value'),
        Input('overlay-dropdown', 'value'),
    ]
)
def set_graph(day, hour, shown_points, mgrs_coords, map_overlay):
    center = mgrs2latlon(mgrs_coords)
    filtered = entries[
        (entries.day == day) &
        (entries.hour == hour)
    ]
    if shown_points == 'civilians':
        filtered = filtered[~filtered.armed]
    if shown_points == 'hostiles':
        filtered = filtered[filtered.armed]

    traces, layout = generate_graph(filtered, center=center, map_overlay=map_overlay)
    return dict(data=traces, layout=layout)


@app.callback(
    Output('day-slider', 'value'),
    [Input('now-button', 'n_clicks')]
)
def set_current_day(n_clicks):
    if n_clicks:
        return datetime.today().weekday()
    else:
        return default_day


@app.callback(
    Output('hour-slider', 'value'),
    [Input('now-button', 'n_clicks')]
)
def set_current_hour(n_clicks):
    if n_clicks:
        return datetime.now().hour
    else:
        return default_hour


""" Running """
if __name__ == '__main__':
    # app.run_server(debug=True)  # dev
    app.run_server(port=80, debug=False)  # prod
