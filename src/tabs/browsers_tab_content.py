import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from src.tabs.tab_content import TabContent

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def __bar_data(position3d, size=(1, 1, 1)):
    bar = np.array([[0, 0, 0],
                    [1, 0, 0],
                    [1, 1, 0],
                    [0, 1, 0],
                    [0, 0, 1],
                    [1, 0, 1],
                    [1, 1, 1],
                    [0, 1, 1]], dtype=float)
    bar *= np.asarray(size)
    bar += np.asarray(position3d)
    return bar


def __triangulate_bar_faces(positions, sizes=None):
    if sizes is None:
        sizes = [(1, 1, 1)] * len(positions)
    else:
        if isinstance(sizes, (list, np.ndarray)) and len(sizes) != len(positions):
            raise ValueError('Your positions and sizes lists/arrays do not have the same length')
    all_bars = [__bar_data(pos, size) for pos, size in zip(positions, sizes) if size[2] != 0]
    p, q, r = np.array(all_bars).shape
    vertices, ixr = np.unique(np.array(all_bars).reshape(p * q, r), return_inverse=True, axis=0)
    I = []
    J = []
    K = []
    for k in range(len(all_bars)):
        I.extend(np.take(ixr,
                         [8 * k, 8 * k + 2, 8 * k, 8 * k + 5, 8 * k, 8 * k + 7, 8 * k + 5, 8 * k + 2, 8 * k + 3,
                          8 * k + 6, 8 * k + 7, 8 * k + 5]))
        J.extend(np.take(ixr,
                         [8 * k + 1, 8 * k + 3, 8 * k + 4, 8 * k + 1, 8 * k + 3, 8 * k + 4, 8 * k + 1, 8 * k + 6,
                          8 * k + 7, 8 * k + 2, 8 * k + 4, 8 * k + 6]))
        K.extend(np.take(ixr,
                         [8 * k + 2, 8 * k, 8 * k + 5, 8 * k, 8 * k + 7, 8 * k, 8 * k + 2, 8 * k + 5, 8 * k + 6,
                          8 * k + 3, 8 * k + 5, 8 * k + 7]))
    return vertices, I, J, K


def __get_plotly_mesh3d(x, y, z, bargap=0.05):
    xedges = np.arange(len(x) + 1)
    yedges = np.arange(len(y) + 1)
    xsize = xedges[1] - xedges[0] - bargap
    ysize = yedges[1] - yedges[0] - bargap
    xe, ye = np.meshgrid(xedges[:-1], yedges[:-1])
    ze = np.zeros(xe.shape)
    positions = np.dstack((xe, ye, ze))
    m, n, p = positions.shape
    positions = positions.reshape(m * n, p)
    sizes = np.array([(xsize, ysize, h) for h in z.flatten()])
    vertices, I, J, K = __triangulate_bar_faces(positions, sizes=sizes)
    X, Y, Z = vertices.T
    return X, Y, Z, I, J, K


def bar3d(x, y, z):
    layout = go.Layout(scene=dict(
        camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=-1, y=1.5, z=0.5)
        ),
        xaxis=dict(
            ticktext=x,
            tickvals=0.5 + np.arange(len(x))
        ),
        yaxis=dict(
            ticktext=y,
            tickvals=0.5 + np.arange(len(y))
        ),
    ))
    fig = go.Figure(layout=layout)
    colors = px.colors.qualitative.Plotly
    for idx in range(len(x)):
        zi = np.zeros_like(z)
        zi[idx, :] = z[idx, :]
        X, Y, Z, I, J, K = __get_plotly_mesh3d(x, y, zi, bargap=0.2)
        mesh3d = go.Mesh3d(x=X, y=Y, z=Z, i=I, j=J, k=K, color=colors[idx], flatshading=True, hoverinfo='skip')
        fig.add_trace(mesh3d)
    return fig


class BrowsersTabContent(TabContent):
    def __init__(self):
        self.browsers = pd.read_csv(os.path.join(THIS_FOLDER, "browsers.csv")).iloc[:4, [0, -1, -2, -3, -4]]

        x = np.array(self.browsers.columns[1:])
        y = self.browsers["Browser"].to_numpy()
        z = self.browsers.iloc[:, 1:].to_numpy()
        self.bad_fig = bar3d(x, y, z)
        self.bad_fig.update_layout(
            scene=dict(
                xaxis_title='Year',
                yaxis_title='Browser',
                zaxis_title='% of market')
        )

        self.good_fig = px.bar(
            self.browsers.melt(id_vars=["Browser"], var_name="year", value_name="perc"),
            x="year",
            y="perc",
            color="Browser",
            barmode="group"
        )
        self.good_fig.update_layout(
            yaxis_title="% of market",
            xaxis_title="Year"
        )

    def get_title(self):
        return "Desktop Browser Market Share"

    def get_desc(self):
        return """
        This is chart of percentage of market share of top 4 desktop browsers
        for last 4 years.
        Maybe showing it on 3D bar plot looks kinda cool,
        but makes it very hard to compare or read.
        """

    def get_form_data(self):
        return [
            ("Which browser was more popular in 2018? IE or Safari?", "IE"),
            ("What % of market had Firefox in 2019 (rounded to 5%)?", "10%"),
            ("Was % of market owned by Firefox in 2018 more or less than 10%? (yes or no)", "yes")
        ]

    def get_bad_figure(self):
        return self.bad_fig

    def get_good_figure(self):
        return self.good_fig
