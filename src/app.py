# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import visdcc

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
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
            html.Section(
                id="intro-section",
                className="section",
                children=[
                    html.Button(
                        id="start-button",
                        children="Get started"
                    ),
                    dcc.Location(id="loc")
                ]
            ),
            html.Section(
                id="main-section",
                className="section",
                children=[
                    html.H1(children='CHOOSE PLOT'),
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
                ]
            ),
            html.Div(id='scroll-blocker', className='scroll'),
        ]),
    visdcc.Run_js(id='javascript',
                  run='''
                        new fullScroll({
                            mainElement: "main",
                            sections: ["intro-section", "main-section"],
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


if __name__ == '__main__':
    app.run_server(debug=True)
