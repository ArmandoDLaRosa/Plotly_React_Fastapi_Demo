import os

import dash
import flask
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output


def create_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
    """
    """
    server = flask.Flask(__name__)
    server.secret_key = os.environ.get('secret_key', 'secret')
    details = {
        'Date': ['2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28', '2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28', '2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28'],
        'Students': ['BHU', 'BHU', 'BHU', 'BHU', 'JNU', 'JNU', 'JNU', 'JNU', 'DU', 'DU', 'DU', 'DU'],
        'Grade': [80, 90, 35, 55, 56, 77, 66, 45, 80, 90, 35, 55],
    }
    df = pd.DataFrame(details)

    app = dash.Dash(__name__, server=server,
                    requests_pathname_prefix=requests_pathname_prefix)

    app.scripts.config.serve_locally = False
    dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

    app.layout = html.Div([
        html.H1('Students'),
        dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'BHU', 'value': 'BHU'},
                {'label': 'JNU', 'value': 'JNU'},
                {'label': 'DU', 'value': 'DU'}
            ],
            value='BHU'
        ),
        dcc.Graph(id='my-graph')
    ], className="container")

    @app.callback(Output('my-graph', 'figure'),
                  [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        dff = df[df['Students'] == selected_dropdown_value]
        return {
            'data': [{
                'x': dff.Date,
                'y': dff.Grade,
                'line': {
                    'width': 3,
                    'shape': 'spline'
                }
            }],
            'layout': {
                'margin': {
                    'l': 30,
                    'r': 20,
                    'b': 30,
                    't': 20
                }
            }
        }

    return app
