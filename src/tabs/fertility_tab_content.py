import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
import json

from src.tabs.tab_content import TabContent

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def lons_lats(geojson):

    def get_center(feature):
        l = feature["geometry"]["coordinates"][0][0]
        x1 = 180
        x2 = 0
        y1 = 180
        y2 = 0
        for (x,y) in l:
            if x < x1:
                x1 = x
            if x > x2:
                x2 = x
            if y < y1:
                y1 = y
            if y > y2:
                y2 = y
        return ((x1+x2)/2, (y1+y2)/2)

    centers = list(map(get_center, geojson["features"]))
    (lons, lats) = ([x[0] for x in centers], [x[1] for x in centers])
    return (lons, lats)

class FertilityTabContent(TabContent):
    def get_title(self):
        return "Fertility in Poland (2017)"

    def get_desc(self):
        return """
        What is the fertility per woman in Poland in 2017 per voivodeship?
        """

    def get_form_data(self):
        return [
            ("Is fertility in Mazowieckie smaller than in Wielkopolskie", "No"),
            ("Is fertility in Łódzkie the smallest", "Yes"),
            ("Is the biggest difference in fertility per voievodeship bigger than 0.3?", "Yes"),
        ]

    def get_bad_figure(self):
        with open(os.path.join(THIS_FOLDER, "voivodeships.geojson"),  encoding='utf-8') as file:
            counties = json.load(file)
        df_chloro = pd.read_csv(os.path.join(THIS_FOLDER, "fertility.csv"))
        fig = px.choropleth(df_chloro, geojson=counties,
                        color="fertility",
                        locations="voivodeship",
                        color_continuous_scale=px.colors.diverging.Armyrose,
                        range_color=[0,3],
                        featureidkey="properties.nazwa",
                        projection="mercator",
                        hover_data={'voivodeship': False, "fertility": False},
                        title="Fertility in Poland in 2017"
                        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def get_good_figure(self):
        with open(os.path.join(THIS_FOLDER, "voivodeships.geojson"),  encoding='utf-8') as file:
            counties = json.load(file)
        df_chloro = pd.read_csv(os.path.join(THIS_FOLDER, "fertility.csv"))
        (lons, lats) = lons_lats(counties)
        df_scatter = pd.DataFrame(
            {"lon": lons,
            "lat": lats,
            "fertility": [str(x) for x in df_chloro["fertility"]]})
        fig = px.choropleth(df_chloro, geojson=counties,
                        color="fertility",
                        locations="voivodeship",
                        color_continuous_scale=px.colors.diverging.Armyrose,
                        featureidkey="properties.nazwa",
                        projection="mercator",
                        hover_data={'voivodeship': True, "fertility": True},
                        labels={"voivodeship": "Voivodeship", "fertility": "Fertility"},
                        title="Fertility in Poland in 2017"
                        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.add_trace({
            "lat": df_scatter["lat"],
            "lon": df_scatter["lon"],
            "text": df_scatter["fertility"],
            "mode": "text",
            "type": "scattergeo",
            "textfont": {
                "size": 16,
                "color": "#000000"
            }
        })
        return fig
