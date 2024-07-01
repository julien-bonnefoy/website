import pandas as pd
import time

euros = {
    "specifier": "$,.2f",
    "locale": {
        "symbol": ["€", " EUR"],
        "group": ".",
        "decimal": ","
    }
}
cols = [
    {'id': 'date_str', 'name': 'Date'},
    {'id': 'type', 'name': 'Type'},
    {'id': 'category', 'name': 'Category'},
    {'id': 'from', 'name': 'From'},
    {'id': 'amount', 'name': 'Amount','type': 'numeric','format': euros},
    {'id': 'to', 'name': 'To'},
    {'id': 'balance', 'name': 'Balance', 'type': 'numeric', 'format': euros}
]

def check_first(df):

    row = df.loc[0]

    if row[0] == 'Date' and row[1] == 'Libellé' and row[2] == 'Débit' and row[3] == 'Crédit' and row[4] == 'Solde':
        df.drop(0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)

    return df


def date_string_to_date(date_string):
    return pd.to_datetime(date_string, infer_datetime_format=True)

def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))


def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix,unit='s')


def getMarks(daterange):
    ''' Returns the marks for labeling.
        Every Nth value will be used.
    '''
    result = {}
    month_nb = 0
    for i, date in enumerate(daterange):
        month = date.month
        if month != month_nb:
            # Append value to dict
            result[unixTimeMillis(date)] = str(date.strftime('%m %Y'))

        month_nb = month
    return result


def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day