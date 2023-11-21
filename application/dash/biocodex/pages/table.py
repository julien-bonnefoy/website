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
    hidden_columns=["lat", "lon", "lun_mat", "lun_am", "mar_mat", "mar_am", "mer_mat", "mer_am", "jeu_mat", "jeu_am", "ven_mat", "ven_am" ],
    style_header={'fontSize': 14, 'font_weight': 900, 'textAlign': 'center', 'color': 'darkblue'},
    style_cell_conditional=[
        {'if': {'column_id': 'id'}, 'textAlign': 'center', 'width': '2%'},
        {'if': {'column_id': 'nom'}, 'textAlign': 'left', 'width': '11%'},
        {'if': {'column_id': 'prenom'}, 'textAlign': 'left', 'width': '5%'},
        {'if': {'column_id': 'spe'}, 'textAlign': 'center', 'width': '2%'},
        {'if': {'column_id': 'pot'}, 'textAlign': 'center', 'width': '2%'},
        {'if': {'column_id': 'pvm'}, 'textAlign': 'center', 'width': '2%'},
        {'if': {'column_id': 'nv22'}, 'textAlign': 'center', 'width': '2%'},
        {'if': {'column_id': 'cib'}, 'textAlign': 'center', 'width': '2%'},
        {'if': {'column_id': 'dec'}, 'textAlign': 'center', 'width': '2%'},
        {'if': {'column_id': 'eta'}, 'textAlign': 'center',  'textOverflow': 'ellipsis', 'fontSize': 12, 'width': '10%'},
        {'if': {'column_id': 'uga'}, 'textAlign': 'center', 'fontSize': 12, 'width': '2%'},
        {'if': {'column_id': 'adr'}, 'textAlign': 'left', 'fontSize': 12, 'width': '11%'},
        {'if': {'column_id': 'cp'}, 'textAlign': 'center', 'fontSize': 12, 'width': '2%'},
        {'if': {'column_id': 'ville'}, 'textAlign': 'left', 'fontSize': 12, 'width': '5%'},
        {'if': {'column_id': 'tel'}, 'textAlign': 'center', 'fontSize': 12, 'width': '5%'},
        {'if': {'column_id': 'mode'}, 'textAlign': 'center', 'fontSize': 12, 'width': '5%'},
        {'if': {'column_id': 'com'}, 'textAlign': 'center', 'fontSize': 12, 'width': '5%'},
        {'if': {'column_id': 'ddv'}, 'textAlign': 'center', 'fontSize': 12, 'width': '5%'},
        {'if': {'column_id': 'dpv'}, 'textAlign': 'center', 'fontSize': 12, 'width': '5%'},
        {'if': {'column_id': 'rdv'}, 'textAlign': 'center', 'fontSize': 12, 'width': '5%'},
        {'if': {'column_id': 'rec'}, 'textAlign': 'center', 'fontSize': 12, 'width': '5%'},
        {'if': {'column_id': 'pk'}, 'textAlign': 'center', 'fontSize': 12, 'width': '5%'},
    ],
    css=[
        {"selector": ".dash-spreadsheet-container tr th", "rule": "height: 16px;"},
        # set height of header
        {"selector": ".dash-spreadsheet-container tr", "rule": "height: 10px;"},
        # set height of body rows
        # {"selector": ".dash-spreadsheet-inner", "rule": "height: calc('100vh - 226px')"}
    ],
    id="tabledash"
)


layout = html.Div(
    [
        dashtable
    ],
    id="table-container"
)
