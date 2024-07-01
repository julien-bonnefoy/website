import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_extensions.enrich import DashProxy
import dash
import importlib
import os

assets_folder= "/var/www/website.julien-bonnefoy.dev/application/static"

external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    dbc.icons.FONT_AWESOME
]

external_scripts = [
    {
        "src": "https://code.jquery.com/jquery-3.7.1.js",
        "integrity": "sha256-eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4=",
        "crossorigin": "anonymous"
    },
    {
        "src":"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
        "crossorigin": "anonymous"
    }
]


def dash_apps_factory(server):
    dashapp_list = [
        {
            'name': 'iris',
            'callback_file': 'callbacks',
            'callback_function': 'init_callbacks',
            'layout_file': 'layout',
            'layout_function': 'build_layout',
            'url': '/dash/iris/',
            'title': 'Iris',
            'use_pages': False,
            'pages_folder': ""
        },
        {
            'name': 'crossfilter',
            'callback_file': 'callbacks',
            'callback_function': 'init_callbacks',
            'layout_file': 'layout',
            'layout_function': 'build_layout',
            'url': '/dash/crossfilter/',
            'title': 'Crossfilter',
            'use_pages': False,
            'pages_folder': ""
        },
        {
            'name': 'biocodex',
            'callback_file': 'callbacks',
            'callback_function': 'init_callbacks',
            'layout_file': 'layout',
            'layout_function': 'build_layout',
            'url': '/dash/biocodex/',
            'title': 'Biocodex',
            'use_pages': True,
            'pages_folder': "biocodex/pages"
        }
    ]
    """Create a Plotly Dash dashboard."""

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}


    for dashapp in dashapp_list:

        callback_function = getattr(
             importlib.import_module(
                 'application.dash.' + dashapp['name'] + '.' + dashapp['callback_file']), dashapp['callback_function'])

        layout_function = getattr(
            importlib.import_module(
                 'application.dash.' + dashapp['name'] + '.' + dashapp['layout_file']), dashapp['layout_function'])

        dash_app = DashProxy(
            __name__,
            server=server,
            url_base_pathname=dashapp['url'],
            meta_tags=[meta_viewport],
            external_stylesheets=external_stylesheets,
            external_scripts=external_scripts,
            use_pages=dashapp['use_pages'],
            pages_folder=dashapp['pages_folder'],
            suppress_callback_exceptions=True,
            assets_folder=assets_folder
        )


        with server.app_context():
            dash_app.title = dashapp['title']
            dash_app.layout = html.Div(
                [
                    dcc.Location(id='url', refresh=False),
                    html.Div(id='page-layout', children=layout_function())
                ]
            )
            callback_function(dash_app)
            # dash_app.run_server(dev_tools_hot_reload=True, debug=True, threaded=True)

    return server
