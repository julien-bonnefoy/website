import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash
import importlib

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
]


def dash_apps_facrory(server):
    """Create a Plotly Dash dashboard."""

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp_list = [
        {
            'name': 'iris',
            'callback_file': 'callbacks',
            'callback_function': 'init_callbacks',
            'layout_file': 'layout',
            'layout_function': 'build_layout',
            'url': '/dash/iris/',
            'title': 'Iris'
        },
        {
            'name': 'crossfilter',
            'callback_file': 'callbacks',
            'callback_function': 'init_callbacks',
            'layout_file': 'layout',
            'layout_function': 'build_layout',
            'url': '/dash/crossfilter/',
            'title': 'CrossfilterS'
        },
        {
            'name': 'orange',
            'callback_file': 'callbacks',
            'callback_function': 'init_callbacks',
            'layout_file': 'layout',
            'layout_function': 'build_layout',
            'url': '/dash/orange/',
            'title': 'Orange'
        }
    ]

    for dashapp in dashapp_list:

        callback_function = getattr(
             importlib.import_module(
                 'flask_app.dash.' + dashapp['name'] + '.' + dashapp['callback_file']), dashapp['callback_function'])

        layout_function = getattr(
            importlib.import_module(
                 'flask_app.dash.' + dashapp['name'] + '.' + dashapp['layout_file']), dashapp['layout_function'])

        dash_app = dash.Dash(
            __name__,
            server=server,
            url_base_pathname=dashapp['url'],
            meta_tags=[meta_viewport],
            external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=True
        )

        with server.app_context():
            dash_app.title = dashapp['title']
            dash_app.layout = html.Div([
                dcc.Location(id='url', refresh=True),
                html.Div(id='page-layout', children=layout_function())
            ])
            dash_app.run_server(dev_tools_hot_reload=True)
            callback_function(dash_app)

    return server
