# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab1',
        children=[
            dcc.Tab(
                label='Tab one',
                value='tab1',
            ),
            dcc.Tab(
                label='Tab two',
                value='tab2',
            ),
            dcc.Tab(
                label='Tab three',
                value='tab3'
            ),
            dcc.Tab(
                label='Tab four',
                value='tab4'
            ),
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
