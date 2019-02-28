import dash
import dash_core_components as dcc
import dash_html_components as html
from plot_factory import traces, layout


app = dash.Dash(__name__)
server = app.server
# styling in external_stylesheets

app.layout = html.Div(children=[
    dcc.Graph(
        id='expected-activity-map',
        figure=dict(data=traces, layout=layout),
        config=dict(displaylogo=False),
    )
])


if __name__ == '__main__':
    app.run_server(debug=True, port=80)  # remove debug (and hot reloading) for production
