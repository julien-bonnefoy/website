from sklearn import datasets
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc


iris_raw = datasets.load_iris()
iris_df = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])

controls = dbc.Card(
    [
        dbc.InputGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[{"label": col, "value": col} for col in iris_df.columns],
                    value="sepal length (cm)",
                    className="w-100"
                ),
            ]
        ),
        dbc.InputGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[{"label": col, "value": col} for col in iris_df.columns],
                    value="sepal width (cm)",
                    className="w-100"
                ),
            ]
        ),
        dbc.InputGroup(
            [
                dbc.Label("Cluster count"),
                dbc.Input(id="cluster-count", type="number", value=3, className="w-100")
            ]
        ),
    ],
    body=True,

)

