import dash_bootstrap_components as dbc
import dash_html_components as html
from config import basedir
from os import path
import base64

FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
image_filename = "flask_app/dash/orange/assets/orange_150.png"

encoded_image = base64.b64encode(open(image_filename, 'rb').read())

sidebar_buttons = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Button(
                    [
                        html.Span(
                            [
                                html.Span(className="hamburger-inner"),
                            ],
                            className="hamburger-box border-0"
                        )
                    ],
                    id="sidebar-toggle",
                    className="hamburger is-active border-0",
                ),
                dbc.Button(
                    [
                        html.Span(
                            [
                                html.Span(className="hamburger-inner"),
                            ],
                            className="hamburger-box"
                        )
                    ],
                    id="navbar-toggle",
                    className="hamburger is-active",
                )
            ],
            className="d-flex flex-row-reverse border-0"
        )
    ]
)

sidebar_header = dbc.Row(
    [
        dbc.Col(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), className="d-flex w-25"),
                html.H3("DASH-OL", className="d-flex")
            ]
        )
    ],
    className="sidebar-header"
)

sidebar = html.Div(
    [
        sidebar_buttons,
        sidebar_header,
        dbc.Collapse(
            [
                html.Hr(),
                dbc.Nav(
                    [
                        dbc.NavLink(
                            html.Span("Home"),
                            href="/dash/orange/",
                            active="exact",
                        ),
                        dbc.NavLink(
                            html.Span("Dashboard"),
                            href="/dash/orange/dashboard/",
                            active="exact",
                        ),
                        dbc.NavLink(
                            html.Span("Mots-clés"),
                            href="/dash/orange/keywords/",
                            active="exact",
                        ),
                    ],
                    vertical=True,
                    pills=True,
                )
            ],
            id="collapse",
        )
    ],
    id="sidebar",
    className="collapsed"
)


def build_sidebar():
    return sidebar


