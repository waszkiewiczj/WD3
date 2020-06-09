# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import visdcc

external_stylesheets = [
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
                    html.Div(id='tabs-content')
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


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab4':
        return html.Div([
            html.H3('Tab content 4')
        ])
    elif tab == 'tab5':
        return html.Div([
            html.H3('Tab content 5')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
