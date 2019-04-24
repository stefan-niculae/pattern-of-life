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
    'Tokyo':    (35.6, 139.7),
    'Yokohama': (35.26, 139.38),
    'Osaka':    (34.41, 135.30),
}

religious_events = [
    'Setsubun (Feb 2)',
    'Hina Matsuri (Mar 3)',
    'Birth of Buddha (Apr 8)',
    'Tanabata Matsuri (Jul 7)',
    'Shichi-go-san (Nov 15)',
]

holidays = [
    'New Year (Jan 1)',
    'Foundation Day (Feb 11)',
    'Vernal Equinox (Mar 21)',
    'Showa Day (Apr 29)',
    'Constitution Memorial (May 3)',
    'Greenery Day (May 4)',
    'Children\'s Day (May 5)',
    'Marine Day (Jul 16)',
    'Mountain Day (Aug 11)',
    'Autumnal Equinox (Sep 23)',
    'Sports Day (Oct 8)',
    'Thanksgiving (Nov 23)',
    'Emperor\'s Birthday (Dec 23)',
]

entries = pd.read_csv('entries.csv')


""" Layout """
traces, layout = generate_graph(entries)  # initial graph

# TODO? make these dynamic as well
counts_range = min(entries.counts), max(entries.counts)

default_day = (0, 4)
default_hour = (9, 17)
default_temperature = (1, 6)


app.layout = html.Div(id='main-container', children=[
    html.Div(id='left-panel', children=[
        html.H1('Expected Activity'),


        # html.H2('Location'),
        #
        # html.P('Area:', className='control-label'),
        # dcc.Dropdown(
        #     id='area-dropdown',
        #     options=[dict(label=city, value=city) for city in city_coords.keys()],
        #     value='Tokyo',
        # ),
        #
        # html.P('MGRS coordinates:', className='control-label'),
        # dcc.Input(
        #     id='mgrs-input',
        #     placeholder='example: 42SWC0920097642',
        #     type='text',
        #     value='',
        # ),

        html.H2('Time'),

        html.P('Day of week:', className='control-label'),
        html.Img(src='assets/day_hist.png', className='slider-hist'),
        dcc.RangeSlider(
            id='day-slider',
            min=0, max=6, step=1,
            value=default_day,
            marks=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        ),

        html.P('Hour of day:', className='control-label'),
        html.Img(src='assets/hour_hist.png', className='slider-hist'),
        dcc.RangeSlider(
            id='hour-slider',
            min=0, max=23, step=1,
            value=default_hour,
            marks={i: i for i in list(range(0, 24, 3)) + [23]},
        ),

        # html.Button('Set current day & hour', id='now-button'),

        html.H2('Weather'),

        html.P('Temperature:', className='control-label'),
        html.Img(src='assets/temperature_bin_hist.png', className='slider-hist'),
        dcc.RangeSlider(
            id='temperature-slider',
            min=0, max=10, step=1,
            value=default_temperature,
            marks={x: f'{t}°' for x, t in zip(range(0, 11, 2), range(50, 75+1, 5))},
        ),

        # html.P('Precipitation:', className='control-label'),
        # dcc.Slider(
        #     id='precipitation-slider',
        #     min=0, max=100, step=.05,
        #     value=default_hour,
        #     marks={x: f'{x}%' for x in range(0, 101, 20)},
        # ),
        #
        #
        # html.H2('Events', id='events-header'),
        #
        # html.P('Religious:', className='control-label'),
        # dcc.Dropdown(
        #     id='religious-dropdown',
        #     options=[dict(label=x, value=x) for x in religious_events],
        #     value=None,
        # ),
        #
        # html.P('Holidays:', className='control-label'),
        # dcc.Dropdown(
        #     id='holidays-dropdown',
        #     options=[dict(label=x, value=x) for x in holidays],
        #     value=None,
        # ),
        #
        # html.Div(className='wide-container', children=[
        #     # html.P('Set as of:', className='inline-label'),
        #     dcc.DatePickerSingle(
        #         date=None,
        #         placeholder='Set as of date...',
        #         display_format='MMM Do, YYYY',
        #         clearable=True,
        #     ),
        # ]),

        html.H2('Show'),

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
            html.Div('Tweets', className='colorscale-label', id='tweets-label'),
            html.Div(className='colorscale', id='tweets-colorscale', children=[
                html.Div(className='colorscale-ticks', children=[
                    html.P(int(counts_range[0]), className='left-tick'),
                    html.P(sum(counts_range) // 2, className='center-tick'),
                    html.P(int(counts_range[1]), className='right-tick'),
                ])
            ]),
        ]),
    ]),

])


""" Interactivity """
# @app.callback(
#     Output('mgrs-input', 'value'),
#     [Input('area-dropdown', 'value')]
# )
# def set_coords_from_area(area_name):
#     return latlon2mgrs(city_coords[area_name])
#
# # TODO when setting MGRS coords manually, blank out area dropdown


@app.callback(
    Output('map-chart', 'figure'),
    [
        Input('day-slider', 'value'),
        Input('hour-slider', 'value'),
        Input('temperature-slider', 'value'),
        # Input('mgrs-input', 'value'),
        Input('overlay-dropdown', 'value'),
    ]
)
def set_graph(
        day_range,
        hour_range,
        temperature_range,
        # mgrs_coords,
        map_overlay
):
    # center = mgrs2latlon(mgrs_coords)
    filtered = pd.DataFrame(entries[
        entries.day.between(*day_range) &
        entries.hour.between(*hour_range) &
        entries.temperature.between(*temperature_range)
    ].groupby(['lat', 'lon']).counts.mean().round().astype(int)).reset_index()

    traces, layout = generate_graph(
        filtered,
        # center=center,  # TODO put back
        map_overlay=map_overlay)
    return dict(data=traces, layout=layout)


# @app.callback(
#     Output('day-slider', 'value'),
#     [Input('now-button', 'n_clicks')]
# )
# def set_current_day(n_clicks):
#     if n_clicks:
#         return datetime.today().weekday()
#     else:
#         return default_day

#
# @app.callback(
#     Output('hour-slider', 'value'),
#     [Input('now-button', 'n_clicks')]
# )
# def set_current_hour(n_clicks):
#     if n_clicks:
#         return datetime.now().hour
#     else:
#         return default_hour


""" Running """
if __name__ == '__main__':
    # app.run_server(debug=True)  # dev
    app.run_server(port=80, debug=False)  # prod
