import plotly.graph_objs as go
from data_generation import expected

MAPBOX_API_TOKEN = 'pk.eyJ1Ijoic3RlZmFubmljdWxhZSIsImEiOiJjanNvNWVmNWQwamQ1NDltbGtsZzJnYnJ2In0.irMk173YO9pawgW6iu_iCg'


def label_format(row):
    s = f'{row.persons} {row.desc}'
    if row.armed:
        s += '<br>Armed'
    return s

labels = expected.apply(label_format, axis=1)


armed2marker_config = {
    True:  dict(colorscale='Reds',  reversescale=False, showscale=False),
    False: dict(colorscale='Greys', reversescale=True,  showscale=False),
}

civilians_counts = expected.persons[~expected.armed]
civilians_range  = min(civilians_counts), max(civilians_counts)
hostiles_counts  = expected.persons[expected.armed]
hostiles_range   = min(hostiles_counts), max(hostiles_counts)

traces = []
for armed_status in [True, False]:
    mask = (expected.armed == armed_status)
    lats = expected.lat[mask]
    lons = expected.lon[mask]
    color_values = expected.persons[mask]
    subset_labels = labels[mask]

    traces.append(go.Scattermapbox(
        lat=lats,
        lon=lons,

        marker={
            'color': color_values,
            'size': 10,
            **armed2marker_config[armed_status],
        },

        showlegend=False,
        text=subset_labels,
        name='',  # FIXME: how to hide it trace name when using custom hover template
        # hoverinfo='none',
        hovertemplate='(%{lat:.2f}°, %{lon:.2f}°)<br>%{text}'
    ))

layout = dict(
    # title='Expected Activity<br><span style="font-size: 12">(dummy generated data)</span>',
    # height='100vh',
    # width=1000,
    autoscale=False,
    margin=go.layout.Margin(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0,
    ),

    xaxis=dict(hoverformat='.2f'),

    mapbox=dict(
        accesstoken=MAPBOX_API_TOKEN,
        bearing=0,
        center=dict(lat=33.5, lon=67.0),  # afghanistan
        pitch=0,  # "parallel" to our screen, with no angle
        zoom=6,
        style='light',
    ),

    updatemenus=[dict(
        buttons=[
            dict(
                args=['mapbox.style', 'light'],
                label='Simple',
                method='relayout'
            ),
            dict(
                args=['mapbox.style', 'outdoors'],
                label='Terrain',
                method='relayout'
            ),
            dict(
                args=['mapbox.style', 'satellite-streets'],
                label='Satellite',
                method='relayout'
            )
        ],

        direction='up', # expansion
        # position
        x=.02,
        xanchor='left',
        y=.02,
        yanchor='bottom',
    )]
)
