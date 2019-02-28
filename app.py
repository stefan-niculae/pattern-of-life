import dash
import dash_core_components as dcc
import dash_html_components as html
from plot_factory import traces, layout, civilians_range, hostiles_range
import base64

app = dash.Dash(__name__)
server = app.server

cities = """Kabul
Mazar-i-Sharif
Kandahar
Herat
Jalalabad
Kunduz
Ghazni
Lashkargah
Taloqan
Puli Khumri
Khost
Charikar
Sheberghan
Sar-e Pol
Maymana
Chaghcharan
Mihtarlam
Farah
Puli Alam"""


app.layout = html.Div(id='main-container', children=[
    html.Div(id='left-panel', children=[
        html.H1('Expected Activity'),

        html.Div(className='colorscale-container', children=[
            html.Div('Civilians', className='colorscale-label', id='civilians-label'),
            html.Div(className='colorscale', id='civilians-colorscale', children=[
                html.P(civilians_range[0], className='left-range'),
                html.P(civilians_range[1], className='right-range'),
            ]),
        ]),
        html.Div(className='colorscale-container', children=[
            html.Div('Hostiles', className='colorscale-label', id='hostiles-label'),
            html.Div(className='colorscale', id='hostiles-colorscale', children=[
                html.P(hostiles_range[0], className='left-range'),
                html.P(hostiles_range[1], className='right-range'),
            ]),
        ]),


        html.H2('Location'),


        html.P('City:', className='control-label'),
        dcc.Dropdown(
            id='city-dropdown',
            options=[dict(label=city, value=city) for city in cities.split()],
            value='Kabul',
        ),


        html.P('Coordinates:', className='control-label'),
        dcc.Input(
            id='lat-input',
            className='coord-input',
            placeholder='Latitude',
            type='number',
            value='34.32'
        ),
        dcc.Input(
            id='lon-input',
            className='coord-input',
            placeholder='Longitude',
            type='number',
            value='69.10'
        ),

        html.H2('Time'),

        html.P('Hour of day:', className='control-label'),
        dcc.RangeSlider(
            id='hour-of-day-slider',
            min=0, max=24, step=.25,
            value=[9, 17],
            marks={i: i for i in range(0, 25, 3)},
        ),

        html.P('Day of week:', className='control-label'),
        dcc.RangeSlider(
            id='day-of-week-slider',
            min=0, max=6, step=1,
            value=[4, 5],
            marks='MTWTFSS',
        ),


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
            # labelStyle={'display': 'inline-block'},
        ),

        html.P('Map overlay:', className='control-label'),
        dcc.Dropdown(
            id='overlay-dropdown',
            options=[
                dict(label='Simple', value='simple'),
                dict(label='Terrain', value='terrain'),
                dict(label='Satellite', value='satellite'),
            ],
            value='simple',
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
])


if __name__ == '__main__':
    # TODO put port=80 when deploying
    app.run_server(debug=True)  # remove debug (and hot reloading) for production
