import dash_bootstrap_components as dbc
from dash import dcc, html
import dash
import importlib
import os

assets_path = os.getcwd() + "/application/dash/assets"


external_scripts=[
    "https://code.jquery.com/jquery-3.7.0.js",
    {"type": "text/javascript", "src": "assets/js/calendar.js"},
]



external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    dbc.icons.FONT_AWESOME
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

        dash_app = dash.Dash(
            __name__,
            server=server,
            url_base_pathname=dashapp['url'],
            meta_tags=[meta_viewport],
            external_stylesheets=external_stylesheets,
            external_scripts=external_scripts,
            use_pages=dashapp['use_pages'],
            pages_folder=dashapp['pages_folder'],
            suppress_callback_exceptions=True,
            assets_folder=assets_path
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
