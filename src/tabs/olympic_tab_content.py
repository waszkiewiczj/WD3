import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from src.tabs import TabContent


class OlympicTabContent(TabContent):

    def __init__(self):
        self.data = self._read_data()

    def _read_data(self):
        data = pd.read_csv('olympic.csv')

        # filter countries with less than 10 golden medals
        data.loc[data['count'] < 10, 'country'] = 'Other'
        data = data.groupby(['country'], as_index=False).sum()
        data['count'] = round(100 * data['count'] / data['count'].sum(), 2)
        data = data.sort_values(by=['count'], ascending=False)

        # move other to the end
        data = data.query('country != \'Other\'').append(data.query('country == \'Other\''))
        return data

    def get_title(self):
        return 'London 2012 Summer Olympics'

    def get_desc(self):
        return """
        Golden medals by countries on 2012 Summer Olympics in London.\n
        Countries with less than 10 golden medals are aggregated to "Other" label.
        """

    def get_form_data(self):
        return [
            ('Who got more: Germany or Russia?', 'Russia'),
            ('What percent of total got United States?', '23'),
            ('What percent of total got Australia?', '3'),
        ]

    def get_bad_figure(self):
        fig = go.Figure(
            data=go.Pie(
                labels=self.data['country'],
                values=self.data['count'],
                textinfo='label',
                hoverinfo='none',
            ),
            layout=go.Layout(height=600)
        )
        return fig

    def get_good_figure(self):
        fig = px.bar(
            self.data,
            x='country',
            y='count',
            color='country',
            title='Golden medals - London 2012',
            labels={'country': 'Country', 'count': 'Percent of total golden medals'},
            height=600
        )
        return fig
