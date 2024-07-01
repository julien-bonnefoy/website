import dash
from .functions import create_time_series, df, groups, format_indicator
import plotly.graph_objs as go

countries = []
for country in df['Country Name'].unique():
    if country not in groups:
        countries.append(country)


def init_callbacks(dash_app):
    @dash_app.callback(
        dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
        dash.dependencies.Output("title", "children"),
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
        dash.dependencies.Input('crossfilter-year', 'value'),
        dash.dependencies.Input('country-name', 'value'))
    def update_graph(xaxis_column_name, yaxis_column_name,
                     xaxis_type, yaxis_type,
                     year_value, selected):

        dff = df[df['Year'] == year_value]

        i1, i1_cut, i1_formated = format_indicator(xaxis_column_name)
        i2, i2_cut, i2_formated = format_indicator(yaxis_column_name)

        fig = go.Figure()

        fig.layout = go.Layout(
            xaxis={
                'title': i1_formated,
                'type': 'linear' if xaxis_type == ' Linear ' else 'log'
            },
            yaxis={
                'title': i2_formated,
                'type': 'linear' if yaxis_type == ' Linear ' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            hovermode="closest",
            showlegend=True
        )

        divided_dict = {}
        for el in ['countries', 'groups', 'selected']:
            divided_dict[el] = {}
            if el == "selected":
                divided_dict[el]["value"] = [selected]
                divided_dict[el]["color"] = "red"
                divided_dict[el]["opacity"] = 1
            if el == "countries":
                divided_dict[el]["value"] = countries
                divided_dict[el]["color"] = "blue"
                divided_dict[el]["opacity"] = 0.33
            if el == "groups":
                divided_dict[el]["value"] = groups
                divided_dict[el]["color"] = "yellow"
                divided_dict[el]["opacity"] = 0.33

            divided_dict[el]["x"] = \
                dff[(dff['Indicator Name'] == i1) & (dff["Country Name"].isin(divided_dict[el]["value"]))]["Value"]
            divided_dict[el]["y"] = \
                dff[(dff['Indicator Name'] == i2) & (dff["Country Name"].isin(divided_dict[el]["value"]))]["Value"]
            divided_dict[el]["text"] = \
                dff[(dff['Indicator Name'] == i2) & (dff["Country Name"].isin(divided_dict[el]["value"]))][
                    "Country Name"]
            divided_dict[el]["customdata"] = \
                dff[(dff['Indicator Name'] == i2) & (dff["Country Name"].isin(divided_dict[el]["value"]))][
                    "Country Name"]

            fig.add_trace(
                go.Scatter(
                    x=divided_dict[el]["x"],
                    y=divided_dict[el]["y"],
                    customdata=divided_dict[el]["customdata"],
                    text=divided_dict[el]["text"],
                    mode='markers',
                    marker=dict(
                        size=15,
                        opacity=divided_dict[el]["opacity"],
                        line={'width': 0.5, 'color': 'black'},
                        color=divided_dict[el]["color"]
                    ),
                    hovertemplate='<b>%{customdata}</b><br><br>' +
                                  f'{i1_cut}: <b>' +
                                  '%{x}</b><br>' +
                                  f'{i2_cut}: <b>' +
                                  '%{y}</b><extra></extra>',
                    name=el
                ))

        return fig, f"{i1_cut}".upper() + " vs. " + f"{i2_cut} - Worldwide".upper()

    @dash_app.callback(
        dash.dependencies.Output('x-time-series', 'figure'),
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
        dash.dependencies.Input('country-name', 'value'))
    def update_x_timeseries(xaxis_column_name, axis_type, country_name):
        dff = df[df['Country Name'] == country_name]
        dff = dff[dff['Indicator Name'] == xaxis_column_name]
        _, _, i1_formated = format_indicator(xaxis_column_name)
        return create_time_series(dff, axis_type, i1_formated,  color="#570e82")

    @dash_app.callback(
        dash.dependencies.Output('y-time-series', 'figure'),
        dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
        dash.dependencies.Input('country-name', 'value'))
    def update_y_timeseries(yaxis_column_name, axis_type, country_name):
        dff = df[df['Country Name'] == country_name]
        dff = dff[dff['Indicator Name'] == yaxis_column_name]
        _, _, i2_formated = format_indicator(yaxis_column_name)
        return create_time_series(dff, axis_type, i2_formated, color="#196010")

    @dash_app.callback(
        dash.dependencies.Output('country-name', 'value'),
        dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
        dash.dependencies.State('country-name', 'value'))
    def update_country(clickData, country_name):
        country_name = clickData['points'][0]['customdata'] if clickData else country_name
        return country_name

    return dash_app
