import dash_core_components as dcc
import dash_html_components as html
from flask_app.dash.orange.pages.sidebar import sidebar

meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=1"}]

content = html.Div(id="page-content", className="pt-0")

app_layout = html.Div(
    [
        dcc.Location(id='orange-url', refresh=False),
        sidebar,
        content
    ],
    id="wrapper"
)


def build_layout():
    return app_layout
