import plotly.graph_objs as go
from dash.dependencies import Input, Output
from .functions import iris_df
from random import sample
from math import fsum, sqrt
from collections import defaultdict
from functools import partial

def mean(data):
    'Accurate arithmetic mean'
    if isinstance(data,list)==False:
        data = list(data)
    return fsum(data) / len(data)

def transpose(matrix):
    'Swap rows with columns for a 2-D array'
    return zip(*matrix)

def distance(p, q, sqrt=sqrt, fsum=fsum, zip=zip):
    'Multi-dimensional euclidean distance between points p and q'
    return sqrt(fsum((x1 - x2) ** 2.0 for x1, x2 in zip(p, q)))

def assign_data(centroids, data):
    'Assign data the closest centroid'
    d = defaultdict(list)
    for point in data:
        centroid = min(centroids, key=partial(distance, point))
        d[centroid].append(point)
    return dict(d)

def compute_centroids(groups):
    'Compute the centroid of each group'
    return [tuple(map(mean, transpose(group))) for group in groups]

def k_means(data, k=2, iterations=10):
    'Return k-centroids for the data'
    data = list(data)
    centroids = sample(data, k)
    for i in range(iterations):
        labeled = assign_data(centroids, data)
        centroids = compute_centroids(labeled.values())
    return centroids

def quality(labeled):
    'Mean value of squared distances from data to its assigned centroid'
    return mean(distance(c, p) ** 2 for c, pts in labeled.items() for p in pts)




def init_callbacks(dash_app):

    @dash_app.callback(
        Output("cluster-graph", "figure"),
        [
            Input("x-variable", "value"),
            Input("y-variable", "value"),
            Input("cluster-count", "value")
        ]
    )
    def make_graph(x, y, n_clusters):
        # minimal input validation, make sure there's at least one cluster

        df = iris_df.loc[:, [x, y]]
        km = k_means(df.values, k=max(n_clusters, 1))

        centers = km

        data = [
            go.Scatter(
                x=df.loc[df.cluster == c, x],
                y=df.loc[df.cluster == c, y],
                mode="markers",
                marker={"size": 8},
                name="Cluster {}".format(c),
            )
            for c in range(n_clusters)
        ]

        data.append(
            go.Scatter(
                x=centers[:, 0],
                y=centers[:, 1],
                mode="markers",
                marker={"color": "#000", "size": 12, "symbol": "diamond"},
                name="Cluster centers",
            )
        )

        layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}

        return go.Figure(data=data, layout=layout)

    # functionality is the same for both dropdowns, so we reuse filter_options
    @dash_app.callback(
        Output("x-variable", "options"),
        [Input("y-variable", "value")],
    )
    # make sure that x and y values can't be the same variable
    def filter_optionsX(v):
        return [{"label": col, "value": col, "disabled": col == v} for col in iris_df.columns]

    @dash_app.callback(
        Output("y-variable", "options"),
        [Input("x-variable", "value")],
    )
    def filter_optionsY(v):
        return [{"label": col, "value": col, "disabled": col == v} for col in iris_df.columns]

    return dash_app
