import dash_bootstrap_components as dbc
from dash import dcc, html
from .functions import df, available_indicators, graph_config, groups
import textwrap


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

tab_content_style = {
    'backgroundColor': '#e0f5ff',
}

com = [
    dbc.Row([
        dbc.Col([
            html.H6(id="title", style={"text-align": "center"}, className="mt-1 mb-0")
        ], className="col-7 offset-1"),
        dbc.Col([
            html.H6("Year", style={"text-align": "center"},  className="mt-1 mb-0")
        ], className="col-1"),
        dbc.Col([
            dcc.Dropdown(
                id='crossfilter-year',
                options=[{"label": year, "value": year} for year in df['Year'].unique()],
                value=2015
            )
        ], className="col-2")
    ], className="my-3"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                config=graph_config,
                hoverData={'points': [{'customdata': 'France'}]},
                style={"height": '50vh'}
            )
        ], className="col-10 offset-1")
    ])
]

sep = [
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='x-time-series', config=graph_config, style={"height": '50vh'}),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in [' Linear ', ' Log ']],
                value=' Linear ',
                labelStyle={'display': 'inline'},
                className="col-4 offset-4"
            ),
        ], className="col-6"),
        dbc.Col([
            dcc.Graph(id='y-time-series', config=graph_config, style={"height": '50vh'}),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in [' Linear ', ' Log ']],
                value=' Linear ',
                labelStyle={'display': 'inline'},
                className="col-4 offset-4"
            ),
        ], className="col-6")
    ],
        style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': '#e0f5ff)',
            'padding': '25px 25px 0px 25px'
        }
    )
]

content = dbc.Container([

    html.H1("DASH CROSSFILTER EXAMPLE"),

    dbc.Row([

        dbc.Col([
            html.H5("Country or Group", style={"text-align": "center"},  className="mb-0")
        ], className="d-flex justify-content-center col-2"),

        dbc.Col([
            dcc.Dropdown(
                id='country-name',
                options=[{"label": country, "value": country} for country in df['Country Name'].unique()],
                value="France"
            )
        ], className="col-2"),

        dbc.Col([
            html.H6("Indicator 1", style={"text-align": "center"},  className="mb-0")
        ], className="col-1"),

        dbc.Col([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': textwrap.shorten(text=i, width=38, placeholder="..."), 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            )
        ], className="col-3"),

        dbc.Col([
            html.H6("Indicator 2", style={"text-align": "center"}, className="mb-0")
        ], className="col-1"),

        dbc.Col([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            )
        ], className="col-3")

    ], className="d-flex align-items-center mb-2"),

    html.Hr(),

    dcc.Tabs([
        dcc.Tab(label="Indicators 1 & 2 Separately", children=sep, style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label="Indicator 1 vs. Indicator 2", children=com,  style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles, content_style=tab_content_style)

], fluid=True)


def build_layout():
    return content



