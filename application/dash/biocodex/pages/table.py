from dash import dash_table, html
import dash
from application.dash.biocodex.functions import datatable_cols, styles


dash.register_page(__name__, path="/table")

dashtable = dash_table.DataTable(
    columns=datatable_cols,
    page_size=20,
    sort_action="native",
    sort_mode="multi",
    filter_action='native',
    page_action='native',
    style_table={'overflowX': 'auto', 'fontSize': 12, 'fontFamily': '"Source Sans Pro", Helvetica, sans-serif'},
    style_data={"color": "black"},
    style_data_conditional=styles,
    hidden_columns=[
        "spe2", "lat", "lon", "lun_m", "lun_a", "mar_m", "mar_a", "mer_m", "mer_a", "jeu_m", "jeu_a", "ven_m", "ven_a" ,
        "c24c1", "c24c2", "c23c3", "nv23", "veeva_link", "ameli_link", "ddvs", "cib", "mode", "rec", "motif", "lieux", "mail"    ],
    style_header={'fontSize': 14, 'font_weight': 900, 'textAlign': 'center', 'color': 'darkblue'},
    style_cell_conditional=[
        {'if': {'column_id': 'id'}, 'textAlign': 'center'},
        {'if': {'column_id': 'nom'}, 'textAlign': 'left'},
        {'if': {'column_id': 'pre'}, 'textAlign': 'left'},
        {'if': {'column_id': 'spe1'}, 'textAlign': 'center'},
        {'if': {'column_id': 'pot'}, 'textAlign': 'center'},
        {'if': {'column_id': 'pvm'}, 'textAlign': 'center'},
        {'if': {'column_id': 'nv22'}, 'textAlign': 'center'},
        {''
         'if': {'column_id': 'age'}, 'textAlign': 'center'},
        {'if': {'column_id': 'dec'}, 'textAlign': 'center'},
        {'if': {'column_id': 'eta'}, 'textAlign': 'center',  'textOverflow': 'ellipsis', 'fontSize': 12},
        {'if': {'column_id': 'uga'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'adr'}, 'textAlign': 'left', 'fontSize': 12},
        {'if': {'column_id': 'cp'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'vil'}, 'textAlign': 'left', 'fontSize': 12},
        {'if': {'column_id': 'tel'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'mode'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'com'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'ddv'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'rdv'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'rdv'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'rec'}, 'textAlign': 'center', 'fontSize': 12},
        {'if': {'column_id': 'motif'}, 'textAlign': 'center', 'fontSize': 12},
    ],
    css=[
        {"selector": ".dash-spreadsheet-container tr th", "rule": "height: 16px;"},
        {"selector": ".dash-spreadsheet-menu", "rule": "position: absolute; bottom: -30px"},
        {"selector": ".show-hide-menu", "rule": "flex-direction: row"},
        {"selector": ".dash-spreadsheet-container tr", "rule": "height: 10px;"},
        # set height of body rows
        # {"selector": ".dash-spreadsheet-inner", "rule": "height: calc('100vh - 226px')"},

    ],
    id="tabledash",
    fill_width=False
)


layout = html.Div(
    [
        dashtable
    ],
    id="table-container"
)
