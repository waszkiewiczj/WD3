import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

from src.tabs.tab_content import TabContent


class StatesTabContent(TabContent):
    def get_title(self):
        return "Population of USA states"

    def get_desc(self):
        return """
        Which state in USA have a highest population? Which one have the lowest? 
        """

    def get_form_data(self):
        return [
            ("What is a postal code of the most populated state?", "CA"),
            ("What is a postal code of the least populated state?", "WY"),
        ]

    def get_bad_figure(self):
        data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv")
        fig = go.Figure(data=go.Scatter(x=data['Postal'],
                                        y=data['Population'],
                                        mode='markers',
                                        marker=dict(
                                            size=8,
                                            color=data['Population'],  # set color equal to a variable
                                            colorscale='Inferno',  # one of plotly colorscales
                                        ),
                                        text=data['State']))  # hover text goes here

        fig.update_layout(title='Population of USA states', xaxis_title="State postal abbreviation",
                          yaxis_title="Population of state", )

        return fig

    def get_good_figure(self):
        data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv")
        data = data.sort_values(by=['Population'], ascending=False)
        fig = go.Figure([go.Bar(x=data['Postal'], y=data['Population'])])

        fig.update_layout(title='Population of USA States', xaxis_title="State postal abbreviation",
                          yaxis_title="State population")

        return fig
