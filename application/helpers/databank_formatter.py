from tqdm.notebook import tqdm
import pandas as pd
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import numpy as np


df = pd.read_csv('../flask_app/data/databank_indicators.csv')
df.drop(['Country Code', 'Series Code'], axis=1, inplace=True)
df.columns = ["Country Name", "Indicator Name", "1960", "1965", "1970", "1975", "1980", "1985", "1990", "1995", "2000", "2005", "2010", "2015", "2020"]
df.drop(df[df['Country Name'].isna()].index, inplace=True)
df.drop(df[df['Indicator Name'].isna()].index, inplace=True)
dtf = df.copy()

dico = {}
for country in tqdm(dtf['Country Name'].unique()):
    print(f"{country}", end="                                                            \r")
    dico[country] = {}
    for indicator in dtf['Indicator Name'].unique():
        dico[country][indicator] = {}
        for year in ["1960", "1965", "1970", "1975", "1980", "1985", "1990", "1995", "2000", "2005", "2010", "2015", "2020"]:
            if dtf[(dtf['Country Name'] == country) & (dtf['Indicator Name'] == indicator)][f"{year}"].values[0]:
                dico[country][indicator][year] = {
                    "Value": dtf[(dtf['Country Name'] == country) & (dtf['Indicator Name'] == indicator)][f"{year}"].values[0]
                }

keys = {
    (country, indicator, year): dico[country][indicator][year]
    for country in dico.keys()
    for indicator in dico[country].keys()
    for year in dico[country][indicator].keys()
}

mux = pd.MultiIndex.from_tuples(keys.keys())

dtf = pd.DataFrame(list(keys.values()), index=mux)

dtf.reset_index(inplace=True)

dtf.columns = ["Country Name", "Indicator Name", "Year", "Value"]

dtf["Value"] = np.where(dtf["Value"] == '..', float("NaN"), dtf["Value"])

dtf["Value"] = dtf["Value"].astype(float)

dtf["Year"] = dtf["Year"].astype(int)

dtf.to_csv('../flask_app/data/databank_indicators_reshaped.csv')
