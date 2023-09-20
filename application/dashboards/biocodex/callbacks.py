from .functions import join_id_adr_cdb, build_one, get_info
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import current_user
from .layout import table_content, map_content, button
import dash_bootstrap_components as dbc
from ..sidebar import sidebar1, sidebar2

df=join_id_adr_cdb()


def init_callbacks(dashapp):

    @dashapp.callback(
        Output('page-content', 'children'),
        Input('biocodex-url', 'pathname'),

    )
    def display_page(pathname):
        if pathname == "/dash/biocodex/table/":
            return [sidebar1, table_content]

        elif pathname == '/dash/biocodex/map/':
            return [sidebar2, map_content]
        """
        elif pathname == "/dash/orange/keywords/":
            return kw_content
        elif pathname == "/dash/orange/categories/":
            return
        """
        # If the users tries to reach a different page, return a 404 message
        return


    @dashapp.callback(
        Output('memory', 'data'),
        Input('uga-cl', 'value'),
        Input("spe-cl", "value"),
        Input('ciblage-check', 'value'),
    )
    def filter(ugas_selected, spe_selected, ciblage_selected):
        if not ugas_selected and not spe_selected and not ciblage_selected:
            # Return all the rows on initial load/no country selected.
            return df.to_dict('records')

        filtered = df.query('uga in @ugas_selected').query('spe in @spe_selected').query('ciblage in @ciblage_selected')

        return filtered.to_dict('records')

    @dashapp.callback(
        Output('datatable', 'data'),
        Output("tile-content", "children"),
        Input('memory', 'data')
    )
    def on_data_set_table(data):
        if data is None:
            raise PreventUpdate
        return data, [build_one(row) for row in data]


    @dashapp.callback(
        Output('user-store', 'data'),
        Input('my-dropdown', 'value'),
        State('user-store', 'data'))
    def cur_user(args, data):
        if current_user.is_authenticated:
            return current_user.user

    @dashapp.callback(
        Output('username', 'children'),
        Input('user-store', 'data'))
    def username(data):
        if data is None:
            return ''
        else:
            return f'Hello {data}'

    @dashapp.callback(
        Output("offcanvas", "is_open"),
        Input("open-offcanvas", "n_clicks"),
        [State("offcanvas", "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if n1:
            return not is_open
        return is_open

    @dashapp.callback(
        Output("sidebar-toggle", "className"),
        Output("sidebar", "className"),
        Output("table-col", "className"),
        Output("page-content", "style"),
        Output("tile-content", "style"),
        [Input("sidebar-toggle", "n_clicks")],
        [State("sidebar", "className")],
    )
    def toggle_classname(n, classname):
        if n and classname != "":
            return "hamburger hamburger--collapse is-active", "", "col-10", {"margin-left":"15rem", "margin-right": "2rem", "transition": "margin-left 0.3s ease-in-out"}, {"width":"85%"}
        return "hamburger hamburger--collapse", "collapsed", "col-11", {"margin-left":"6rem", "margin-right": "2rem", "transition": "margin-left 0.3s ease-in-out"}, {"width": "92.5%"}

    @dashapp.callback(
        Output("sidebar-body-collapse", "is_open"),
        [Input("navbar-toggle", "n_clicks")],
        [State("sidebar-body-collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open, {"width": "calc('100%-8rem');"}
        return is_open, {"width": "100%"}

    @dashapp.callback(
        Output('modal', 'children'),
        Output('modal', 'is_open'),
        Input('datatable', 'active_cell'),
        Input('close', 'n_clicks'),
        State("modal", "is_open")
    )
    def update_modal(active_cell, n_clicks, is_open):
        print("active_cell: ", active_cell)
        print("n_clicks: ", n_clicks)
        print("is_open: ", is_open)
        if active_cell:
            row = df.iloc[[active_cell.get("row")]]
            return [
                    dbc.ModalHeader(row['nom'].values[0]),
                    dbc.ModalBody("This will be something more interesting"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ml-auto")
                    ),
                ], not is_open
        elif n_clicks:
            return [], is_open
        else:
            return [], False

    @dashapp.callback(
        Output("uga-geojson", "hideout"),
        Input("uga-cl", "value"),
        State("uga-geojson", "hideout"),
    )
    def toggle_select(ugas_selected, uga_hideout):
        uga_hideout["selected"] = ugas_selected
        return uga_hideout

    @dashapp.callback(
        Output("pharma-geojson", "hideout"),
        Input("uga-cl", "value"),
        State("pharma-geojson", "hideout")
    )
    def toggle_select(ugas_selected, pharma_hideout):
        pharma_hideout["ugas_selected"] = ugas_selected
        return pharma_hideout

    @dashapp.callback(
        Output("target-geojson", "hideout"),
        Input("uga-cl", "value"),
        Input("spe-cl", "value"),
        State("target-geojson", "hideout")
    )
    def toggle_select(ugas_selected, spes_selected, target_hideout):
        target_hideout["ugas_selected"] = ugas_selected
        target_hideout["spes_selected"] = spes_selected
        return target_hideout

    @dashapp.callback(
        Output("untarget-geojson", "hideout"),
        Input("uga-cl", "value"),
        Input("spe-cl", "value"),
        State("untarget-geojson", "hideout")
    )
    def toggle_select(ugas_selected, spes_selected, untarget_hideout):
        untarget_hideout["ugas_selected"] = ugas_selected
        untarget_hideout["spes_selected"] = spes_selected
        return untarget_hideout

    @dashapp.callback(
        Output("info", "children"),
        Input("uga-geojson", "hoverData")
    )
    def info_hover(feature):
        return get_info(feature)
