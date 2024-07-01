from dash import html, dash_table
import dash_bootstrap_components as dbc
import dash
from ..helpers.styles import FLEX_STYLE
from ..helpers.helpers import cols


dash.register_page(__name__, path="/table")


title_div = html.Div(
    [
        html.H1('LYDIA ACCOUNT', className="text-center")
    ]
)

table_col = dbc.Col(
    [
        dash_table.DataTable(
            id="statement-table",
            page_size=25,
            columns=cols,
            fixed_rows={'headers': True},
            style_header={
                'backgroundColor': 'darkblue',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'color': 'white'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'date_str'},
                 'width': '10%', 'textAlign': 'center'},
                {'if': {'column_id': 'type'},
                 'width': '5%', 'textAlign': 'left'},
                {'if': {'column_id': 'category'},
                 'width': '15%', 'textAlign': 'left'},
                {'if': {'column_id': 'from'},
                 'width': '20%', 'textAlign': 'center'},
                {'if': {'column_id': 'amount'},
                 'width': '10%'},
                {'if': {'column_id': 'to'},
                 'width': '20%', 'textAlign': 'center'},
                {'if': {'column_id': 'balance'},
                 'width': '10%'},
            ]
        )
    ]
)

layout = html.Div(
    [
        title_div,
        dbc.Row(
            [
                table_col
            ]
        )
    ]
)