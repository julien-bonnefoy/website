import plotly.graph_objs as go
import pandas as pd
from ...config import basedir
from os import path
import re

df = pd.read_csv(path.join(basedir, "data/csv/databank_indicators_reshaped.csv"))

available_indicators = df['Indicator Name'].unique()

groups = ['Arab World', 'Africa Eastern and Southern', 'Africa Western and Central', 'Caribbean small states',
          'Central Europe and the Baltics', 'Early-demographic dividend',
          'East Asia & Pacific',
          'East Asia & Pacific (excluding high income)',
          'East Asia & Pacific (IDA & IBRD countries)', 'Euro area',
          'Europe & Central Asia',
          'Europe & Central Asia (excluding high income)',
          'Europe & Central Asia (IDA & IBRD countries)', 'European Union',
          'Fragile and conflict affected situations',
          'Heavily indebted poor countries (HIPC)', 'High income',
          'IBRD only', 'IDA & IBRD total', 'IDA blend', 'IDA only',
          'IDA total', 'Late-demographic dividend',
          'Latin America & Caribbean',
          'Latin America & Caribbean (excluding high income)',
          'Latin America & the Caribbean (IDA & IBRD countries)',
          'Least developed countries: UN classification',
          'Low & middle income', 'Low income', 'Lower middle income',
          'Middle East & North Africa',
          'Middle East & North Africa (excluding high income)',
          'Middle East & North Africa (IDA & IBRD countries)',
          'Middle income', 'North America', 'Not classified', 'OECD members',
          'Other small states', 'Pacific island small states',
          'Post-demographic dividend', 'Pre-demographic dividend',
          'Small states', 'South Asia', 'South Asia (IDA & IBRD)',
          'Sub-Saharan Africa', 'Sub-Saharan Africa (excluding high income)',
          'Sub-Saharan Africa (IDA & IBRD countries)', 'Upper middle income',
          'World']

graph_config = {
    'modeBarButtonsToRemove': [
        'sendDataToCloud',
        'pan2d',
        'zoomIn2d',
        'zoomOut2d',
        'autoScale2d',
        'resetScale2d',
        'hoverCompareCartesian',
        'hoverClosestCartesian',
        'toggleSpikelines'
    ],
    'displayModeBar': False,
    'displaylogo': False
}


def create_time_series(dff, axis_type, title, color):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers',
            line=dict(color=color)
        )],
        'layout': {
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'yaxis': {'type': 'linear' if axis_type == ' Linear ' else 'log'},
            'xaxis': {'showgrid': False},
            "title": {
                'text': title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'bottom',
                'font': {"color": color}
            }
        }
    }


def format_indicator(indicator):
    pattern = re.compile("(\(.*\)|, total|, value added)")
    repl = ""
    ind_cut = re.sub(pattern, repl, indicator)
    if re.search(pattern, indicator):
        opt = re.search("\(.*\)", indicator).group(0)
        ind_formated = ind_cut + f"\n{opt}"
    return indicator, ind_cut, ind_formated
