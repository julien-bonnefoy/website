from ipywidgets import HBox, VBox, Accordion, Tab, Layout, Textarea, widgets
from ipywidgets.embed import embed_data
import plotly
import pandas as pd
import plotly.graph_objs as go
from .colors import plasma_10
from .lo_columns import index_subset, type_subset, skill_subset, rule_subset
from .lo_columns import description_subset, provider_subset, time_subset
import textwrap
import json

html_template = """
<html>
  <head>

    <title>Widget export</title>

    <!-- Load RequireJS, used by the IPywidgets for dependency management -->
    <script 
      src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js" 
      integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" 
      crossorigin="anonymous">
    </script>

    <!-- Load IPywidgets bundle for embedding. -->
    <script
      data-jupyter-widgets-cdn="https://unpkg.com/"
      data-jupyter-widgets-cdn-only
      src="https://cdn.jsdelivr.net/npm/@jupyter-widgets/html-manager@*/dist/embed-amd.js" 
      crossorigin="anonymous">
    </script>

    <!-- The state of all the widget models on the page -->
    <script type="application/vnd.jupyter.widget-state+json">
      {manager_state}
    </script>
  </head>

  <body>

    <div id="">
      <!-- This script tag will be replaced by the view's DOM tree -->
      <script type="application/vnd.jupyter.widget-view+json">
        {widget_views[0]}
      </script>
    </div>

  </body>
</html>
"""


def pie(df, column_name, pie_type, height=175):
    labels = []
    values = []
    colors = []
    pull = []

    if pie_type == "cat_pie":
        cat_names = df[column_name].dropna().unique()
        labels = [textwrap.shorten(cat_name, 30, placeholder="...") for cat_name in cat_names]
        values = df[column_name].value_counts()
        colors = plasma_10[:len(labels)]
        pull = None
    elif pie_type == "empty_pie":
        total_rows = df.shape[0]
        filled = df[column_name].describe(include='all')['count']
        empty = total_rows - filled
        labels = ['empty', 'non empty']
        values = [empty, filled]
        colors = ['#ff7900', '#46039f']
        pull = [0.2, 0]

    fig = go.FigureWidget(
        data=[go.Pie(
            labels=labels,
            values=values,
            textinfo='percent',
            hoverinfo='label+value',
            textposition='inside',
            showlegend=True,
            pull=pull,
            marker=dict(
                colors=colors,
                line=dict(
                    color='#000000',
                    width=1
                )
            ))
        ]
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=height
    )

    return fig


def summarize(df):
    total_rows = df.shape[0]
    summary = {}

    for col in df.columns:

        data_type = df[col].dtype
        column_description = df[col].describe(include='all')
        filled_rows = int(column_description['count'])
        filled_perc = round((filled_rows / total_rows * 100), 3)
        empty_rows = int(total_rows - filled_rows)
        empty_perc = int(empty_rows / total_rows * 100)

        # EMPTY
        if filled_perc < 96.0:
            empty_fig = pie(df, col, "empty_pie")
            # empty_fig.show()
        else:
            empty_fig = float('NaN')

        empty_warning = float("Nan")
        if 75.0 <= filled_perc < 95.0:
            empty_warning = "nv. 1"
        elif 50.0 <= filled_perc < 75.0:
            empty_warning = "nv. 2"
        elif 25.0 <= filled_perc < 50.0:
            empty_warning = "nv. 3"
        elif 0.0 <= filled_perc < 25.0:
            empty_warning = "nv. 4"

        summary[f'{col}'] = {
            'data type': data_type,
            'filled rows': filled_rows,
            'filled rate': str(filled_perc) + "%",
            'empty rows': empty_rows,
            'empty rate': str(empty_perc) + "%",
            'empty fig': empty_fig,
            'empty warning': empty_warning
        }

        if data_type == 'float64':
            summary[f'{col}'].update(
                [
                    ('mean', column_description['mean']),
                    ('std', column_description['std']),
                    ('min', column_description['max']),
                    ('25%', column_description['25%']),
                    ('50%', column_description['50%']),
                    ('75%', column_description['75%']),
                    ('max', column_description['max']),
                ]
            )

        elif data_type == 'object':
            unique = int(column_description['unique'])
            if unique < 10:
                fig = pie(df, col, "cat_pie")
                # fig.show()
                summary[f'{col}'].update(
                    [
                        ('nb of uniques', str(unique)),
                        ('fig', fig),
                    ]
                )

            if filled_rows == 0:
                unique_ratio = float('NaN')
            else:
                unique_ratio = int(column_description['unique'] / filled_rows * 100)

            if unique_ratio > 90:
                top = column_description['top']
                freq = str(column_description['freq'])
                summary[f'{col}'].update(
                    [
                        ('index-like warning', 'index-like'),
                        ('most uused', top),
                        ('most used count', freq)
                    ]
                )

    summary_df = pd.DataFrame.from_dict(summary, orient='index')

    return summary_df


def build_vbox(dico, width='100%'):
    box_list = []
    for k, v in dico.items():
        if str(v) != 'NaN':
            if isinstance(v, plotly.graph_objs.FigureWidget):
                hbox = widgets.Box([v], layout=Layout(height='auto', width='100%'))
            else:
                widget001 = widgets.HTML(value=k, layout=Layout(height='auto', width='50%'))
                widget002 = widgets.HTML(value=str(v), layout=Layout(height='auto', width='50%'))
                hbox = HBox(children=[widget001, widget002])

            box_list.append(hbox)

        vbox = VBox(children=box_list, layout=Layout(width=width))

        return vbox


def build_accordion(variables):
    vbox_list = []
    accordion = Accordion(selected_index=None, style='danger')
    for idx, col in enumerate(variables.keys()):
        accordion.set_title(idx, str(col))
        vbox_list.append(build_vbox(variables[col]))
    accordion.children = vbox_list

    return accordion


def build_widget(df, subset):
    summary_dict = {}
    for index, column in enumerate(subset):
        summary_dict[f'{column}'] = widgets.HTML(value=column, layout=Layout(height='auto', width='100%'))

    overview_column_list = VBox([value for value in summary_dict.values()])

    df_copy = df[subset].copy()
    summary_df = summarize(df_copy)

    variables = {}
    for column_name in summary_df.index:
        variables[f'{column_name}'] = summary_df.loc[column_name]

    main_tab_names = ['Columns', 'Overview']
    main_tab = Tab()

    for idx, name in enumerate(main_tab_names):
        main_tab.set_title(idx, str(name))

    variables_accordion = build_accordion(variables)
    overview = Tab()
    overview.children = [overview_column_list, Textarea(width='100%')]
    overview.set_title(0, 'Selection')
    overview.set_title(1, 'Warnings')

    banner = widgets.HTML(
        '<p style="color: #ff7900; text-align: center; font-weight: bold; font-size:20px; '
        'line-height:30px">SELECTION </p> '
    )
    main_tab.children = [variables_accordion, overview]

    return banner, main_tab


def build_mega_accordion(df):
    banner, index_widget = build_widget(df, index_subset)
    banner, type_widget = build_widget(df, type_subset)
    banner, skill_widget = build_widget(df, skill_subset)
    banner, rule_widget = build_widget(df, rule_subset)
    banner, description_widget = build_widget(df, description_subset)
    banner, provider_widget = build_widget(df, provider_subset)
    banner, time_widget = build_widget(df, time_subset)

    accordion = widgets.Accordion(selected_index=None)
    accordion.children = [index_widget, type_widget, skill_widget,
                          rule_widget, description_widget, provider_widget, time_widget]
    labels = ['About INDEX', 'About TYPE', 'About SKILLS',
              'About RULES', 'About DESCRIPTIONS', 'About PROVIDER',
              'About TIME']

    for idx, child in enumerate(labels):
        accordion.set_title(idx, child)

    return accordion


def export_widget(widget):
    data = embed_data(views=[widget.widget])
    manager_state = json.dumps(data['manager_state'])
    widget_views = [json.dumps(view) for view in data['view_specs']]
    rendered_template = html_template.format(manager_state=manager_state, widget_views=widget_views)
    with open(f'{widget.name}_export.html', 'w') as file:
        file.write(rendered_template)
    return


class MegaAccordion(object):
    def __init__(self, name, df):
        self.name = name
        self.widget = build_mega_accordion(df)
