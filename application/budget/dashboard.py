import dash_bootstrap_components as dbc
from dash import html, dcc, Dash, Input, Output, State
from budget.pages.partials import sidebar, navbar
import plotly.graph_objects as go
import plotly.express as px
from budget.helpers.styles import SIDEBAR_STYLE, SIDEBAR_HIDEN, CONTENT_STYLE, CONTENT_STYLE1
import dash
import pandas as pd
import plotly.express as px
from budget.pages.filters import   csv_fn


# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True, pages_folder="budget/pages", suppress_callback_exceptions=True)


content = html.Div(
    [
        dash.page_container
    ],
    id="page-content",
    style=CONTENT_STYLE
)

app.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        navbar,
        sidebar,
        content
    ]
)

@app.callback(
    Output('graph-content', 'figure'),
    Input('category-dd', 'value'),
    Input('months-dd', 'value'),
)
def update_graph(cat_value, time_value):

    df = pd.read_csv(csv_fn, sep=";", keep_default_na=False, parse_dates=['date_dt'], dayfirst=True)

    if not time_value and not cat_value:
        pos = df[df["amount"] > 0].sort_values(by="date_dt")
        neg = df[df["amount"] < 0].sort_values(by="date_dt")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=pos["year_mth"], y=pos["amount"], histfunc="sum", name="INCOME"))
        fig.add_trace(go.Histogram(x=neg["year_mth"], y=-neg["amount"], histfunc="sum", name="OUTCOME"))
        fig.update_layout(legend=dict(orientation="h", xanchor="center", x=0.5));
        return fig

    if time_value:

        if isinstance(time_value, str):
            time_value=[time_value]
        else:
            time_value = time_value

        dff = df[df["year_mth"].isin(time_value)].copy()

    else:
        dff = df.copy()

    if cat_value:

        if isinstance(cat_value, str):
            cat_value=[cat_value]
        else:
            cat_value = cat_value

        dfff = dff[dff["category"].isin(cat_value)].copy()

    else:

        dfff = dff.copy()

    pos = dfff[dfff["amount"] > 0].sort_values(by="date_dt")
    neg = dfff[dfff["amount"] < 0].sort_values(by="date_dt")
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=pos["year_mth"], y=pos["amount"], histfunc="sum", name="INCOME"))
    fig.add_trace(go.Histogram(x=neg["year_mth"], y=-neg["amount"], histfunc="sum", name="OUTCOME"))
    fig.update_layout(legend=dict(orientation="h", xanchor="center", x=0.5))

    return fig




@app.callback(
    Output('statement-table', 'data'),
    Input('category-dd', 'value'),
    Input('months-dd', 'value'),
)
def update_table(cat_value, time_value):

    df = pd.read_csv(csv_fn, sep=";", keep_default_na=False, parse_dates=['date_dt'], dayfirst=True)

    if not time_value and not cat_value:

        table = df.sort_values(by="date_dt", ascending=False).copy()
        table = table[["date_str", "type", "category", "from", "amount", "to", "balance"]]
        data = table.to_dict("records")

        return data

    else:

        if time_value:

            if isinstance(time_value, str):
                time_value=[time_value]
            else:
                time_value = time_value

            dff = df[df["year_mth"].isin(time_value)].copy()

        else:
            dff = df.copy()

        if cat_value:

            if isinstance(cat_value, str):
                cat_value=[cat_value]
            else:
                cat_value = cat_value
            print(cat_value)
            dfff = dff[dff["category"].isin(cat_value)].copy()

        else:

            dfff = dff.copy()

        table = dfff.sort_values(by="date_dt", ascending=False)
        table = table[["date_str", "type", "category", "from", "amount", "to", "balance"]]
        data = table.to_dict("records")

        return data

@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

if __name__ == '__main__':
    app.run(debug=True)