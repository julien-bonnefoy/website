import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from wordcloud import WordCloud
from io import BytesIO
import base64
from app.helpers.graphs import multi_color_func
from app.helpers.colors import plasma_15
from app.helpers.lo_columns import columns, names
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
from dash_table import DataTable
import numpy as np
from app.helpers.preprocess_text import get_top_n_words, get_top_n2_words
import re
import ast
from config import basedir
from os import path

pd.options.display.max_colwidth = None
cols_dict = dict(zip(columns, names))


def get_value_counts(df, column, match=None):
    if match:
        return df[column].value_counts()[match]
    return df[column].value_counts()


def make_local_df(df, column, choice):
    supplier_df = df[df[column] == choice]
    return supplier_df


def make_counter_row(df, column, name):
    if column == "lo_id":
        orange_line = None
        black_line = dbc.Col([html.Hr(id="hr_black")], className="px-0")
        qty = dbc.Col(
            [
                html.H5(
                    ["\u00A0%s" % len(list(df[column].unique()))], id=f"{column}_qty"
                ),
                html.H5(
                    ["\u00A0" + name.upper() + "\u00A0"],
                    id=f"{column}_counter_name"
                )
            ],
            width={"offset": 2},
            className="d-flex flex-row align-items-center h-50"
        )

    else:
        orange_line = dbc.Col([html.Hr(id="hr_orange")], className="px-0 col-2")
        black_line = None
        qty = dbc.Col(
            [
                html.H5(
                    ["\u00A0%s" % len(list(df[column].unique()))], id=f"{column}_qty"
                ),
                html.H5(
                    [ "\u00A0" + name.upper() + "\u00A0"],
                    id=f"{column}_counter_name"
                )
            ],
            className="d-flex flex-row align-items-center pl-0 h-50"
        )

    counter_row = dbc.Row(
        [
            orange_line,
            qty,
            black_line
        ],
        style={"height": "25%"},
        className="d-flex align-items-center"
    )

    return counter_row


def make_footer(content):
    footer = dbc.CardFooter(
        [
            html.P(content)
        ],
        className="w-100 text-center py-2 border-0"
    )
    return footer


def make_dd(df, column):
    options = list(
        {"label": name, "value": name} for name in df[column].dropna().unique()
    )
    options.insert(0, {"label": "tous les fournisseurs".upper(), "value": "ALL"})
    dd_col = dbc.Col(
        [
            dcc.Dropdown(
                id=f"{column}_drop",
                options=options,
                style={
                    "width": "100%",
                    "color": "#000",
                    'display': 'inline-block',
                    "fontWeight": "900"
                },
                clearable=False
            )
        ],
        style={
        },
        className="d-flex flex-column align-items-center justify-content-center my-1 w-100"
    )

    return dd_col


def make_cloud(df, column, view_env, from_frequencies=False, stopwords=[]):
    font_path = path.join(basedir, "app/static/fonts/coolvetica_rg.ttf")

    if not from_frequencies:
        corpus = [' '.join(vocab.split()) if isinstance(vocab, str) else ' '.join(vocab) for vocab in df[column]]
        cloud = WordCloud(
            background_color="white",
            font_path=font_path,
            stopwords=set(stopwords),
            max_words=1000,
            random_state=0,
            max_font_size=90,
            contour_width=1,
            collocations=False,
            height=150
        ).generate(' '.join(corpus))

    elif from_frequencies:
        cloud = WordCloud(
            background_color="white",
            font_path=font_path,
            stopwords=set(stopwords),
            max_words=1000,
            random_state=0,
            max_font_size=90,
            contour_width=1,
            collocations=False,
        ).generate_from_frequencies(df[column].value_counts())

    cloud.recolor(color_func=multi_color_func)

    if view_env == "notebook":
        fig = plt.figure(figsize=[14, 7])
        ax = plt.imshow(cloud, interpolation="bilinear")
        plt.axis("off")

        return fig.show()

    elif view_env == "dash":
        img = BytesIO()
        cloud.to_image().save(img, format='PNG')
        src = "data:image/png;base64,{}".format(base64.b64encode(img.getvalue()).decode())

        return src


def make_histo(df, column, n=10):
    x = df[column].value_counts().keys().tolist()[:n]
    y = df[column].value_counts().values.tolist()[:n]
    fig = go.Figure(
        data=[
            go.Bar(
                x=x,
                y=y,
                text=y,
                insidetextfont=dict(color="#fff"),
                # textfont=dict(size=20),
                hovertemplate='<b>%{label}</b><br>%{value}<extra></extra>',
                textposition='inside',
                marker=dict(
                    color=[plasma_15[i] for i in range(n)],
                    line=dict(
                        color='#000000',
                        width=1
                    )
                )
            )
        ],
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            autosize=True,
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            xaxis=dict(showticklabels=False),
            hoverlabel=dict(
                bgcolor="#000",
                font=dict(
                    family="Helvetica",
                    #   size=22,
                    color="white",
                )
            )
        )
    )

    return fig


def make_pie(df, column, n=7, showlegend=False):
    labels = df[column].dropna().value_counts().keys().tolist()[:n]
    # labels = [label[:12] for label in labels]
    values = df[column].value_counts().values.tolist()[:n]
    if column == "active_status":
        colors = plasma_15
    elif column == "lo_type":
        colors = plasma_15[2:]
    else:
        colors = plasma_15[::-1]
    # random.shuffle(colors)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo='percent',
                hovertemplate='<b>%{label}</b><br>%{value} L.O.<extra></extra>',
                insidetextorientation="radial",
                textfont=dict(size=16),
                textposition='inside',
                marker=dict(
                    colors=[colors[i] for i in range(n)],
                    line=dict(
                        color='#000000',
                        width=1
                    )
                )
            )
        ],
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            autosize=True,
            showlegend=showlegend,
            margin=dict(t=0, b=0, l=0, r=0),
            legend=dict(
                orientation='v',
                font=dict(size=14),
                yanchor="middle",
                xanchor="left",
                y=0.5,
                x=1
            ),
            hoverlabel=dict(
                bgcolor="#000",
                font=dict(
                    family="Helvetica",
                    # size=18,
                    color="white",
                )
            )
        )
    )

    return fig


def make_sun(df, ind, col_1, col_2, reverse=False):
    sun_df = df[[ind, col_1, col_2]].copy()
    df['tx'] = pd.Series(dtype=float)
    sun_df.columns = [ind, col_1, col_2]

    pivot_sun = sun_df.pivot_table(index=[col_1, col_2], values=ind, aggfunc='count', margins=False)
    ndf = pd.DataFrame(pivot_sun.to_records())

    if reverse:
        fig = px.sunburst(ndf, path=[col_2, col_1], values=ind,
                          color_discrete_sequence=plasma_15[2:])

    else:
        fig = px.sunburst(ndf, path=[col_1, col_2], values=ind,
                          color_discrete_sequence=plasma_15)
    fig.update_traces(
        textinfo='label+percent entry',
        insidetextorientation='radial',
        textfont_size=18,
        hovertemplate='<b>%{parent}</b><br><b>%{label}</b><br>Nb of L.O.: %{value}'
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        autosize=True,
        title_font_size=14,
        margin=dict(t=0, l=0, r=0, b=0),
        hoverlabel=dict(
            bgcolor="#000",
            font=dict(
                family="Coolvetica",
                # size=18,
                color="white"
            )
        )
    )

    return fig


def make_graduated_bar(dtf, column):
    rate = 1 - (len(dtf[dtf[column].isna() == True]) / dtf.shape[0])
    return rate * 10


def make_recap_table(df, ind, col_1, col_2):
    recap_df = df.pivot_table(index=[col_2], values=[ind], columns=col_1, aggfunc='count', margins=True)

    recap_df['taux inactif'] = [round(recap_df.loc[lo_type, (ind, 0)] / (
            recap_df.loc[lo_type, (ind, 0)] + recap_df.loc[lo_type, (ind, 1)]) * 100, 0) for
                                lo_type in recap_df.index]
    recap_df['taux inactif'] = recap_df['taux inactif'].apply(lambda x: f'{int(x)}%' if not np.isnan(x) else 0)

    for column in [1, 0, 'All']:
        recap_df.loc[:, (ind, column)] = recap_df.loc[:, (ind, column)].apply(
            lambda x: f'{int(x)}' if not np.isnan(x) else 0)

    recap_df = pd.DataFrame(recap_df.to_records())
    recap_df[col_2] = recap_df[col_2].apply(lambda x: x.upper())
    recap_df.columns = ['', 'active', 'not_active', 'All', 'taux inactif']
    recap_df = recap_df[['', 'taux inactif']].copy()
    recap_df.set_index('', drop=True)
    table = DataTable(
        id=f"{col_1}_{col_2}_table",
        data=recap_df.to_dict('records'),
        columns=[{'id': c, 'name': c.upper()} for c in recap_df.columns],
        style_as_list_view=True,
        style_data={
            "lineHeight": "1vmin"
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'taux inactif'},
                'textAlign': 'center',
            }
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#ddd'
            }
        ],
        style_header={
            'backgroundColor': '#ff7900',
            'fontWeight': 'bold'
        }
    )
    return table


def make_top_words(df, grams, stopwords=[]):
    n = 10
    docs = [' '.join(vocab_list.split()) for vocab_list in df['lemma_lo_description']]
    colors = plasma_15[:n]
    colors.reverse()
    if grams == 'uni':
        top_words = get_top_n_words
        top_words = top_words(docs, stopwords, n)
        top_df = pd.DataFrame(top_words)
        top_df.columns = ["Word", "Freq"]

        top_words = top_df["Word"][:n].to_list()
        top_words.reverse()
        top_frq = top_df["Freq"][:n].to_list()
        top_frq.reverse()

        top_words = {
            "data": [
                {
                    "y": top_words,
                    "x": top_frq,
                    "type": "bar",
                    "name": "",
                    "orientation": "h",
                    'marker': {'color': colors}
                }
            ],
            "layout": {
                "margin": dict(t=0, b=20, l=100, r=0, pad=0),
            }
        }
        fig = go.Figure(top_words)

        return fig

    elif grams == 'bi':
        top_words = get_top_n2_words
        top_words = top_words(docs, stopwords, n)
        top_df = pd.DataFrame(top_words)
        top_df.columns = ["Word", "Freq"]

        top_words = top_df["Word"][:n].to_list()
        top_words.reverse()
        top_frq = top_df["Freq"][:n].to_list()
        top_frq.reverse()

        top_words = {
            "data": [
                {
                    "y": top_words,
                    "x": top_frq,
                    "type": "bar",
                    "name": "",
                    "orientation": "h",
                    'marker': {'color': colors}
                }
            ],
            "layout": {
                "margin": dict(t=0, b=20, l=100, r=0, pad=0),
                "height": 300

            }
        }
        fig = go.Figure(top_words)

        return fig


def keywords_to_df(keywords):
    kwds = re.sub("'", '"', keywords)
    kw_dict = ast.literal_eval(kwds)
    kwdf = pd.DataFrame.from_dict(kw_dict, orient="index")
    kwdf.reset_index(drop=False, inplace=True)
    kwdf.columns = ["keyword", "score tfidf"]
    return kwdf
