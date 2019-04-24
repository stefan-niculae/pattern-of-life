import plotly.graph_objs as go

MAPBOX_API_TOKEN = 'pk.eyJ1Ijoic3RlZmFubmljdWxhZSIsImEiOiJjanNvNWVmNWQwamQ1NDltbGtsZzJnYnJ2In0.irMk173YO9pawgW6iu_iCg'

TOKYO_COORDS = (35.68, 139.77)


def generate_graph(entries, center=TOKYO_COORDS, map_overlay='light'):
    trace = go.Scattermapbox(
        lat=entries.lat,
        lon=entries.lon,

        marker=dict(
            size=15.5,
            color=entries.counts,
            #       - A list of 2-element lists where the first element is the
            #         normalized color level value (starting at 0 and ending at 1),
            #         and the second item is a valid color string.
            #         (e.g. [[0, 'green'], [0.5, 'red'], [1.0, 'rgb(0, 0, 255)']])
            #       - One of the following named colorscales:
            #             ['Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu',
            #             'Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet',
            #             'Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis', 'Cividis']
            colorscale=[
                # blues
                [0,  'rgba(173, 204, 225, .3)'],
                [.5, 'rgba(70, 128, 184, .7)'],
                [1,  'rgba(19, 50, 106, .95)'],
            ],
            reversescale=False,
            showscale=False,
        ),

        showlegend=False,
        text=entries.counts,
        name='',
        hovertemplate='(%{lat:.2f}°, %{lon:.2f}°)<br>%{text}'
    )

    layout = dict(
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
            center=dict(lat=center[0], lon=center[1]),
            pitch=0,  # "parallel" to our screen, with no angle
            zoom=11,
            style=map_overlay,
        ),
    )

    return [trace], layout
