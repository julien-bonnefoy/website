import dash_bootstrap_components as dbc
from dash import dcc, html
import dash
import importlib
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url


external_scripts=[
    "https://code.jquery.com/jquery-3.7.0.js",
    "https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js",
    "https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js",
    {
        "type": "text/javascript",
        "src": "js/leaflet.extra-markers.min.js"
    },
    {
        "type": "text/javascript",
        "src": "js/modalize.js"
    },
    {
        "type": "text/javascript",
        "src": "js/flipper.js"
    }
]


external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    dbc.icons.FONT_AWESOME,
    # Dash CSS
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css',
    # JQuery DataTables
    "https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css",
    # Leaflet
    {"rel": "stylesheet", "type": "text/css", "src": "css/leaflet.extra-markers.min.css"},
    # Sidebar
    {"rel": "stylesheet","type": "text/css","src": "css/sidebar.css"},
    # Hamburgers
    {"rel": "stylesheet","type": "text/css","src": "css/hamburgers.css"}
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
            suppress_callback_exceptions=True
        )


        with server.app_context():
            dash_app.title = dashapp['title']
            dash_app.layout = html.Div(
                [
                    dcc.Location(id='url', refresh=True),
                    html.Div(id='page-layout', children=layout_function())
                ])
            dash_app.enable_dev_tools(
                debug=True
            )
            callback_function(dash_app)
            # dash_app.run_server(dev_tools_hot_reload=True, debug=True, threaded=True)

    return server
