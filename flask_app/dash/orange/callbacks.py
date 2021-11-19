from .pages.homepage import content as home_content
from .pages.lo_page import content as lo_content
from .pages.keywords import content as kw_content
from .functions import make_sun, make_local_df, make_pie, make_recap_table, make_graduated_bar, make_cloud
from .functions import make_top_words, make_counter_row
from ...helpers.preprocess_text import get_top_n_words
from ...data.orange_data import df, dtf
import pandas as pd
import textwrap
import ast
from dash_table import DataTable
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np

block = {"display": "block"}
flex = {"display": "flex", "justify-content": "center", "align-items": "center"}
flex_col = {"display": "flex-column"}
hide = {"display": "none"}


def init_callbacks(dash_app):
    # DISPLAY CHOSEN PAGE
    @dash_app.callback(
        Output('page-content', 'children'),
        Input('orange-url', 'pathname')
    )
    def display_page(pathname):
        if pathname == "/dash/orange/":
            return home_content
        elif pathname == '/dash/orange/dashboard/':
            return lo_content
        elif pathname == "/dash/orange/keywords/":
            return kw_content
        elif pathname == "/dash/orange/categorie/s":
            return
        # If the users tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger")
            ]
        )

    @dash_app.callback(
        Output("sidebar-toggle", "className"),
        Output("sidebar", "className"),
        [Input("sidebar-toggle", "n_clicks")],
        [State("sidebar", "className")],
    )
    def toggle_classname(n, classname):
        if n and classname != "":
            return "hamburger hamburger--collapse is-active", ""
        return "hamburger hamburger--collapse", "collapsed"

    @dash_app.callback(
        Output("sidebar-body-collapse", "is_open"),
        [Input("navbar-toggle", "n_clicks")],
        [State("sidebar-body-collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @dash_app.callback(
        Output("ol-modal", "is_open"),
        [Input("ol-modal-button", "n_clicks"),
         Input("ol-modal-close", "n_clicks")],
        [State("ol-modal", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dash_app.callback(
        Output("sun-modal", "is_open"),
        [Input("sun-modal-button", "n_clicks"),
         Input("sun-modal-close", "n_clicks")],
        [State("sun-modal", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dash_app.callback(
        Output("lo-modal", "is_open"),
        [Input("lo-modal-button", "n_clicks"),
         Input("lo-modal-close", "n_clicks")],
        [State("lo-modal", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dash_app.callback(
        Output("supplier_drop", "value"),
        [Input("supplier_histo", "clickData")]
    )
    def update_supplier_drop_on_click(clickData):
        if clickData is not None:
            selected_supplier = clickData["points"][0]["x"]
            return selected_supplier
        return "ALL"

    @dash_app.callback(
        Output("lo_id_counter_row", "children"),
        Output("subject_pie", "figure"),
        Input("supplier_drop", "value"),
    )
    def supplier_drop_update(value):
        if value == "ALL" or value is None:
            counter_row = make_counter_row(df, "lo_id", "learning" + "\u00A0" + "objects")
            fig = make_pie(df, "parent_subject", showlegend=True)
            return counter_row, fig
        else:
            local_df = make_local_df(df, "supplier", value)
            counter_row = make_counter_row(local_df, "lo_id", "learning" + "\u00A0" + "objects")
            fig = make_pie(local_df, "parent_subject", showlegend=True)
            return counter_row, fig

    @dash_app.callback(
        Output("active_status_lo_type_sun", "figure"),
        # Output("active_status_lo_type_table_col", "children"),
        Output("active_status_pie", "figure"),
        Output("lo_type_pie", "figure"),
        Input("supplier_drop", "value"),
        Input("order_switch", "value")
    )
    def supplier_drop_update(valueA, valueB):

        if valueA is None:
            valueA = "ALL"

        if valueA != "ALL":
            local_df = make_local_df(dtf, "supplier", valueA)
            active_pie = make_pie(local_df, "active_status", showlegend=True)
            type_pie = make_pie(local_df, "lo_type", showlegend=True)
            if not valueB:
                fig = make_sun(local_df, "lo_id", "active_status", "lo_type", reverse=True)
            else:
                fig = make_sun(local_df, "lo_id", "active_status", "lo_type", reverse=False)
            return fig, active_pie, type_pie

        active_pie = make_pie(dtf, "active_status", showlegend=True)
        type_pie = make_pie(dtf, "lo_type", showlegend=True)
        if not valueB:
            fig = make_sun(dtf, "lo_id", "active_status", "lo_type", reverse=True)
        else:
            fig = make_sun(dtf, "lo_id", "active_status", "lo_type", reverse=False)
        return fig, active_pie, type_pie

    @dash_app.callback(
        Output("order_switch_col", "className"),
        Output("active_status_lo_type_sun_col", "className"),
        # Output("active_status_lo_type_table_col", "className"),
        Output("active_status_pie_col", "style"),
        Output("lo_type_pie_col", "style"),
        Input("view_switch", "value")
    )
    def view_update(value):
        if not value:
            return {}, {}, hide, hide
        return "d-none", "d-none", {}, {}

    @dash_app.callback(
        Output("subject_missing_bar_title", "children"),
        Output("subject_missing_bar", "value"),
        Input("supplier_drop", "value"),
    )
    def update_bar(value):
        if value is None:
            value = "ALL2"

        if value != "ALL":
            local_df = make_local_df(df, "supplier", value)
            rate = make_graduated_bar(local_df, "parent_subject")
            title = f"renseigné à {round(rate * 10)} %".upper()
            return title, rate
        rate = make_graduated_bar(df, "parent_subject")
        title = f"renseigné à {round(rate * 10)} %".upper()
        return title, rate

    @dash_app.callback(
        [
            Output("supplier_selection_bis", "children"),
            Output("kw_cloud", "src"),
            Output("frequency-figure-1", "figure"),
            Output("wc_footer", "children"),
            Output("wc_footer", "style")
        ],
        [
            Input("supplier_drop", "value"),
            Input("switch_knob", "on")
        ],
        [
            State("knob", "value"),
        ]
    )
    def update_cloud_plot(supplier_drop_value, switch_knob_on, knob_value):
        knob_value = round(knob_value)
        children = []
        style_footer = {"display": "none"}
        if supplier_drop_value is not None:
            local_df = make_local_df(dtf, "supplier", supplier_drop_value)
            if switch_knob_on is False:
                fig1 = make_top_words(local_df, grams="uni")
                src = make_cloud(local_df, "lemma_lo_description", "dash")
            else:  # i.e. switch_on is True so rebuild frequency plots
                docs = [' '.join(vocab.split()) if isinstance(vocab, str) else ' '.join(vocab) for vocab in
                        dtf["lemma_lo_description"]]
                top_words = get_top_n_words(docs, n=knob_value)
                top_df = pd.DataFrame(top_words)
                top_df.columns = ["Word", "Freq"]
                add_words = top_df["Word"][:knob_value].to_list()
                fig1 = make_top_words(local_df, grams="uni", stopwords=add_words)
                src = make_cloud(local_df, "lemma_lo_description", "dash", stopwords=add_words)
                children = [html.P("Words removed"), html.P(' '.join(add_words))]
                style_footer = {"display": "block"}

            return supplier_drop_value.upper(), src, fig1, children, style_footer

        else:  # i.e. supplier_value is None
            fig1 = make_top_words(dtf, grams="uni")
            src = make_cloud(dtf, "lemma_lo_description", "dash")
            if switch_knob_on is True:
                docs = [' '.join(vocab.split()) if isinstance(vocab, str) else ' '.join(vocab) for vocab in
                        dtf["lemma_lo_description"]]
                top_words = get_top_n_words(docs, n=knob_value)
                top_df = pd.DataFrame(top_words)
                top_df.columns = ["Word", "Freq"]
                add_words = top_df["Word"][:knob_value].to_list()
                children = [html.P("Words removed"), html.P(' '.join(add_words))]
                style_footer = {"display": "block"}
                fig1 = make_top_words(dtf, grams="uni", stopwords=add_words)
                src = make_cloud(dtf, "lemma_lo_description", "dash", stopwords=add_words)

            return "pas de sélection".upper(), src, fig1, children, style_footer

    @dash_app.callback(
        [Output("freq-body", "is_open"),
         Output("freq-header-expand-btn", "style"),
         Output("freq-header-collapse-btn", "style")],
        [Input("freq-header-expand-btn", "n_clicks"),
         Input("freq-header-collapse-btn", "n_clicks")],
        [State("freq-body", "is_open")]
    )
    def toggle_freq(n1, n2, is_open):
        show = {"display": "block", "margin-bottom": "0px"}
        hide = {"display": "none"}
        if n1 or n2:
            if is_open is False:
                return True, hide, show
            return False, show, hide
        return False, show, hide

    @dash_app.callback(
        [Output("kw-body", "is_open"),
         Output("kw-header-expand-btn", "style"),
         Output("kw-header-collapse-btn", "style")],
        [Input("kw-header-expand-btn", "n_clicks"),
         Input("kw-header-collapse-btn", "n_clicks")],
        [State("kw-body", "is_open")]
    )
    def toggle_kw(n1, n2, is_open):
        show = {"display": "block", "margin-bottom": "0px"}
        hide = {"display": "none"}
        if n1 or n2:
            if is_open is False:
                return True, hide, show
            else:
                return False, show, hide
        else:
            return False, show, hide

    @dash_app.callback(
        [Output('kw-table', 'data'),
         Output('kw-table', 'columns'),
         Output('title-dropdown', 'options'),
         Output('total_lo', 'value'),
         Output('active_lo', 'value'),
         Output('avg_score', 'value')],
        [Input('supplier_drop', 'value')]
    )
    def update_table(value):

        if value is not None:
            data_df = make_local_df(dtf, "supplier", value)

        else:
            data_df = dtf.copy()

        total_lo = len(data_df)
        active_lo = len(data_df[data_df['active_status'] == "actif"])
        avg_score = round(data_df['score_rate'].sum() / total_lo * 100)
        data_df = data_df[["lo_title", 'lo_description', 'tfidf_keywords_global', 'score_global',
                           'rate_global']]
        data_df['rate_global'] = data_df['rate_global'].apply(lambda x: f'{round(float(x) * 100)} %')
        columns = [
            {'id': "lo_title", 'name': "Titre original"},
            {'id': "lo_description", 'name': "Description originale"},
            {'id': "tfidf_keywords_global", 'name': "Mots-clés TF-IDF"},
            {'id': "score_global", 'name': "Score"},
            {'id': "rate_global", 'name': "Score (% du titre)"}
        ]
        data = data_df.to_dict('records')
        options = [{'label': titre, 'value': titre} for titre in data_df['lo_title'].unique()]
        return data, columns, options, total_lo, active_lo, avg_score

    @dash_app.callback(
        [Output('description', 'children'),
         Output('lemma-title', 'children'),
         Output('tfidf-keywords', 'children'),
         Output('lemma-score', 'children'),
         Output('lemma-score-perc', 'children'),
         Output('col1', 'style'),
         Output('col2', 'style'),
         Output('col3', 'style'),
         Output('col4', 'style'),
         Output('col5', 'style')
         ],
        [Input('title-dropdown', 'value')]
    )
    def print_example(value):
        hide = {'display': 'none'}
        block = {'display': 'block'}
        flex = {"display": "flex", "justify-content": "center", "align-items": "center"}
        if value is None:
            return '', '', '', '', '', hide, hide, hide, hide, hide
        else:
            description = dtf.loc[dtf['lo_title'] == value, 'lo_description']
            description = textwrap.fill(description.values[0], max_lines=5, placeholder="  [...]")
            title = dtf.loc[dtf['lo_title'] == value, 'lemma_lo_title']
            keywords = dtf.loc[dtf['lo_title'] == value, 'tfidf_keywords_global']
            keywords_df = pd.DataFrame.from_dict(ast.literal_eval(keywords.values[0]), orient="index")
            keywords_df.reset_index(drop=False, inplace=True)
            keywords_df.columns = ["keywords", "score tfidf"]
            keywords_df['match'] = ['⭐' if keyword in title.values[0].split() else None for keyword in
                                    keywords_df['keywords']]
            table = DataTable(
                id="keywords_table",
                data=keywords_df.to_dict('records'),
                columns=[{'id': c, 'name': c.upper()} for c in keywords_df.columns],
                style_as_list_view=True,
                style_data={
                    "lineHeight": "1vmin"
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'score tfidf'},
                        'textAlign': 'center'
                    }
                ],
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#ddd'
                    }
                ],
                style_header={
                    'backgroundColor': '#ff7900',
                    'fontWeight': 'bold'
                }
            )
            score = dtf.loc[dtf['lo_title'] == value, 'score_global']
            perc = f"{round(float(dtf.loc[dtf['lo_title'] == value, 'rate_global']) * 100)} %"
            return description, title, table, score, perc, block, block, block, block, block

    @dash_app.callback(
        Output("freq-modal", "is_open"),
        [Input("freq-modal-button", "n_clicks"),
         Input("freq-modal-close", "n_clicks")],
        [State("freq-modal", "is_open")],
    )
    def toggle_freq_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dash_app.callback(
        Output("tfidf_modal", "is_open"),
        [Input("tfidf_modal_btn", "n_clicks"),
         Input("tfidf_modal_close_btn", "n_clicks")],
        [State("tfidf_modal", "is_open")],
    )
    def toggle_tfidf_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dash_app.callback(
        Output("datatable_col", "is_open"),
        Output("datatable_btn", "style"),
        Output("datatable_close_btn", "style"),
        [Input("datatable_btn", "n_clicks"),
         Input("datatable_close_btn", "n_clicks")],
        [State("datatable_col", "is_open")],
    )
    def toggle_table(n1, n2, is_open):
        hide = {'display': 'none'}
        show = {'display': 'block'}
        if is_open is False:
            return True, hide, show
        return False, show, hide
