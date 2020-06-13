import plotly.graph_objects as go

import pandas as pd
import os

from src.tabs.tab_content import TabContent


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class CoronavirusTabContent(TabContent):
    def get_title(self):
        return "COVID-19 Active cases"

    def get_desc(self):
        return """
        What is the ratio of active cases of COVID-19 per 1 million people in given country?
        """

    def get_form_data(self):
        return [
            ("Is active cases ratio in Italy approx. 4 times greater than in France?", "No"),
            ("Has France twice the active cases ratio than Germany?", "No"),
            ("Has Spain twice the active cases ratio than Germany?", "Yes"),
        ]

    def get_bad_figure(self):
        data = pd.read_csv(os.path.join(THIS_FOLDER, "coronavirus.csv"))
        fig = go.Figure([go.Bar(x=data['Country'], y=data['Cases_ratio'])])
        fig.update_yaxes(range=[2000, 6000])

        fig.update_layout(title='Active cases of COVID-19 per 1 mln people', xaxis_title="Country",
                          yaxis_title="Active cases per 1 mln", )

        return fig

    def get_good_figure(self):
        data = pd.read_csv(os.path.join(THIS_FOLDER, "coronavirus.csv"))
        data = data.sort_values(by=['Cases_ratio'], ascending=False)
        fig = go.Figure([go.Bar(x=data['Country'], y=data['Cases_ratio'])])

        fig.update_layout(title='Active cases of COVID-19 per 1 mln people', xaxis_title="Country",
                          yaxis_title="Active cases per 1 mln")

        return fig
