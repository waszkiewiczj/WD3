# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Output, Input, State, MATCH
import visdcc
import tabs

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
                        className="text-center",
                        children=[
                            html.H4("Have you ever wondered how bad can people make plots?"),
                            html.H4("Shockingly, very bad."),
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
                        className="div-tab",
                        children=[
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        children=[
                                            dbc.Card(
                                                className="mx-4",
                                                children=[
                                                    html.H3(
                                                        id="title",
                                                        className="card-title"
                                                    ),
                                                    html.P(
                                                        id="desc",
                                                        className="card-text"
                                                    ),
                                                    html.H6("You think is not that bad? Let's find out."),
                                                    html.Div(id="form"),
                                                    html.Button(
                                                        id="check-button",
                                                        children="Check your answers!"
                                                    )
                                                ],
                                                body=True
                                            )
                                        ],
                                        width=4
                                    ),
                                    dbc.Col([
                                        dcc.Graph(id="plot"),
                                        html.Div(
                                            className="text-center",
                                            children=[
                                                "Switch to see ",
                                                html.B("HOW IT'S DONE:")
                                            ]
                                        ),
                                        dbc.Row(
                                            children=[
                                                html.H4("Bad 👎🏼", id="bad-header"),
                                                daq.ToggleSwitch(
                                                    id="plot-switch",
                                                    className="switch",
                                                    value=False
                                                ),
                                                html.H4("Good 👌🏼", id="good-header")
                                            ],
                                            align="center",
                                            justify="center"
                                        )
                                    ], width=8)
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
        Output("form", "children"),
        Output("plot", "figure")
    ],
    [
        Input('tabs', 'value'),
        Input("plot-switch", "value")
    ])
def render_content(tab, good):
    if tab == 'tab1':
        content = tabs.StatesTabContent()
    else:
        content = tabs.ExampleTabContent()
    form = [
        dbc.FormGroup([
            dbc.Label("{}. {}".format(nr + 1, data[0])),
            dbc.Input(
                id={
                    'type': 'form-input',
                    'index': nr
                },
                type="text",
                placeholder="Put your answer here..."
            ),
            dcc.Store(
                id={
                    'type': 'form-answer',
                    'index': nr
                },
                data=data[1]
            )
        ])
        for nr, data in enumerate(content.get_form_data())
    ]
    return [
        content.get_title(),
        content.get_desc(),
        form,
        content.get_good_figure() if good else content.get_bad_figure()
    ]


@app.callback(
    [
        Output({'type': 'form-input', 'index': MATCH}, 'valid'),
        Output({'type': 'form-input', 'index': MATCH}, 'invalid'),
    ],
    [Input("check-button", "n_clicks")],
    [
        State({'type': 'form-input', 'index': MATCH}, 'value'),
        State({'type': 'form-answer', 'index': MATCH}, 'data')
    ]
)
def check_answer(n_clicks, given, true):
    if n_clicks is None:
        return None, None
    if given is None:
        return False, True
    is_true = str.lower(given).lstrip() == str.lower(true).lstrip()
    return is_true, not is_true


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
