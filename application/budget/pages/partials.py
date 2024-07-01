import dash_bootstrap_components as dbc
from dash import html
from budget.helpers.styles import SIDEBAR_STYLE
from .filters import ddowns_col

sidebar = html.Div(
    [
        html.H2("FILTERS", className="display-4"),
        html.Hr(),
        ddowns_col,
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/#", id="home-link"),
                dbc.NavLink("Data table", href="/table", id="table-link"),
                dbc.NavLink("Graph", href="/histo", id="histo-link"),
            ],
            vertical=True,
            pills=True,
        )
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
        dbc.NavItem(dbc.NavLink("Home", href="#")),
        dbc.NavItem(dbc.NavLink("Data table", href="/table")),
        dbc.NavItem(dbc.NavLink("Graph", href="/histo"))
    ],
    brand="Brand",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

