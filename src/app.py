# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Output, Input
import visdcc

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://codepen.io/chriddyp/pen/bWLwgP.css"
]

external_scripts = []

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts
)

app.layout = html.Div([
    html.Div(
        id="main",
        className="scroll-container",
        children=[
            dcc.Location(id="loc"),
            html.Section(
                id="intro",
                className="section section-intro",
                children=[
                    html.Div(
                        style={
                            "text-align": "center"
                        },
                        children=[
                            html.H4("""
                        Have you ever wonder how bad can people make plots?
                        Very bad.
                        """),
                            html.Button(
                                id="start-button",
                                children="Check it out"
                            )
                        ])
                ]
            ),
            html.Section(
                id="plots",
                className="section",
                children=[
                    html.H3(
                        className="header-center",
                        children="Choose plot you want to see. Even if it is ugly as... you know."
                    ),
                    dcc.Tabs(
                        id="tabs",
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
                            dcc.Tab(
                                label='Tab five',
                                value='tab5'
                            )
                        ]
                    ),
                    html.Div(
                        id='tabs-content',
                        style={
                            "padding": "40px"
                        },
                        children=[
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        children=[
                                            dbc.Card([
                                                html.H3(
                                                    id="title",
                                                    className="card-title"
                                                ),
                                                html.P(
                                                    id="desc",
                                                    className="card-text"
                                                ),
                                                dbc.Row(
                                                    children=[
                                                        html.H4("Bad 👎🏼", id="bad-header"),
                                                        daq.ToggleSwitch(
                                                            id="plot-switch",
                                                            style=dict(width="100px"),
                                                            value=False
                                                        ),
                                                        html.H4("Good 👌🏼", id="good-header")
                                                    ],
                                                    align="center",
                                                    justify="center"
                                                )
                                            ],
                                                body=True
                                            )
                                        ],
                                        md=4
                                    ),
                                    dbc.Col(dcc.Graph(id="plot"), md=8)
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(id='scroll-blocker', className='scroll'),
        ]),
    visdcc.Run_js(id='javascript',
                  run='''
                        new fullScroll({
                            mainElement: "main",
                            sections: ["intro", "plots"],
                            displayDots: false
                          });
                        '''
                  )
])


@app.callback(
    Output("loc", "href"),
    [Input("start-button", "n_clicks")]
)
def get_started(n_clicks):
    return "#0" if n_clicks is None else "#1"


@app.callback(
    [
        Output("title", "children"),
        Output("desc", "children"),
        Output("plot", "figure")
    ],
    [
        Input('tabs', 'value'),
        Input("plot-switch", "value")
    ])
def render_content(tab, good):
    return [
        "Title",
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """,
        {
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ]


@app.callback(
    [
        Output("bad-header", "style"),
        Output("good-header", "style"),
        Output("plot-switch", "color")
    ],
    [Input("plot-switch", "value")]
)
def switch_plot(good):
    return [
        dict(color="lightgrey" if good else "red"),
        dict(color="green" if good else "lightgrey"),
        "green" if good else "red"
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
