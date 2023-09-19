import numpy as np
from colorsys import rgb_to_hls
import plotly.graph_objs as go
from .colors import plasma_15
import plotly.express as px
from collections import Counter
from .lo_columns import columns, names
from colour import Color
import pandas as pd

columns_translator = { column: name for column, name in zip(columns, names)}


def multi_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):

    def hex_to_hsl(hex):
        h = hex.lstrip('#')
        rgb = [int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)]
        hsl = rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
        return [int(hsl[0] * 360), int(hsl[2] * 100), int(hsl[1] * 100)]

    colors = [hex_to_hsl(color) for color in plasma_15]

    rand = np.random.randint(0, len(colors) - 1)

    return "hsl({}, {}%, {}%)".format(colors[rand][0], colors[rand][1], colors[rand][2])


Colors = list[str]


def emptiness(df: pd.DataFrame, title: str, colors: Colors) -> px.bar:
    colorscale = []
    for c in colors:
        if isinstance(c, str):
            colorscale.append(c)
        elif isinstance(c, Color):
            colorscale.append(c.hex)

    x = [col for col in df.columns]  # names of the columns
    y = [df[col].count() for col in df.columns]
    fig = px.bar(
        y=y,
        x=x,
        text=[f'{round(yi * 100 / 66517, 1)}' for yi in y],
        color=y,
        color_continuous_scale=colorscale
    )

    fig.update_traces(
        textposition=None,
        textfont_size=14,
        hovertemplate="%{label} <br> %{text} %")

    fig.update_layout(
        hovermode=None,
        hoverlabel=dict(
            bgcolor="#f16e00",
            font_color='#fff',
            font_size=24,
            font_family="Helvetica"
        ),
        xaxis_tickangle=-40,
        height=600,
        title=title,
        yaxis_title="NON EMPTY COUNT",
        xaxis_title="",
        font=dict(
            size=12,
            color="#000"),
        modebar_remove=["autoScale2d", "autoscale", "editInChartStudio", "editinchartstudio", "hoverCompareCartesian",
                        "hovercompare", "lasso", "lasso2d", "orbitRotation", "orbitrotation", "pan", "pan2d", "pan3d",
                        "reset", "resetCameraDefault3d", "resetCameraLastSave3d", "resetGeo", "resetSankeyGroup",
                        "resetScale2d", "resetViewMapbox", "resetViews", "resetcameradefault", "resetcameralastsave",
                        "resetsankeygroup", "resetscale", "resetview", "resetviews", "select", "select2d",
                        "sendDataToCloud", "senddatatocloud", "tableRotation", "tablerotation", "toImage",
                        "toggleHover", "toggleSpikelines", "togglehover", "togglespikelines", "toimage", "zoom",
                        "zoom2d", "zoom3d", "zoomIn2d", "zoomInGeo", "zoomInMapbox", "zoomOut2d", "zoomOutGeo",
                        "zoomOutMapbox", "zoomin", "zoomout"]
    )
    return fig


def make_pie(df, column_name, dico=None, max_cat=7, no_na=True, width=500, height=250, show_legend=True):
    if no_na:
        counter = Counter(df[column_name].dropna()).most_common()
    else:
        counter = Counter(df[column_name]).most_common()

    labels = [name[:30] for name, _ in counter]
    values = [count for _, count in counter]

    if dico:
        for key, value in dico.items():
            if column_name == value:
                column_name = key

    if len(labels) > max_cat:
        labels = labels[:max_cat]
        values = values[:max_cat]
        title = f'TOP {max_cat}  \u00AB {column_name.upper()} \u00BB'
    else:
        title = f'{column_name.upper()}'

    # build pie chart
    fig = go.FigureWidget(
        data=[go.Pie(
            labels=labels,
            values=values,
            textinfo='percent',
            hoverinfo='label+value+percent',
            hoverlabel=dict(font_size=16, font_color='white'),
            showlegend=show_legend,
            textposition='inside',
            marker=dict(
                colors=plasma_15,
                line=dict(
                    color='#000000',
                    width=1
                )
            ))
        ]
    )
    fig.update_layout(
        title=title,
        margin=dict(t=50, b=0),
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        width=width,
        height=height)

    return fig
