import plotly.graph_objs as go

MAPBOX_API_TOKEN = 'pk.eyJ1Ijoic3RlZmFubmljdWxhZSIsImEiOiJjanNvNWVmNWQwamQ1NDltbGtsZzJnYnJ2In0.irMk173YO9pawgW6iu_iCg'


def label_format(row):
    return f'{row.counts} {row.kind}'

armed2marker_config = {
    True:  dict(colorscale='Reds',  reversescale=False, showscale=False),
    False: dict(colorscale='Greys', reversescale=True,  showscale=False),
}
armed2name = {
    True: 'Hostile',
    False: 'Civilian',
}


def generate_graph(entries, center=(33.5, 67.0), map_overlay='light'):
    labels = entries.apply(label_format, axis=1)

    traces = []
    for armed_status in [True, False]:
        mask = (entries.armed == armed_status)
        lats = entries.lat[mask]
        lons = entries.lon[mask]
        color_values = entries.counts[mask]
        subset_labels = labels[mask]

        traces.append(go.Scattermapbox(
            lat=lats,
            lon=lons,

            marker={
                'color': color_values,
                'size': 15,
                **armed2marker_config[armed_status],
            },

            showlegend=False,
            text=subset_labels,
            name=armed2name[armed_status],
            hovertemplate='(%{lat:.2f}°, %{lon:.2f}°)<br>%{text}'
        ))

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
            zoom=6,
            style=map_overlay,
        ),
    )

    return traces, layout
