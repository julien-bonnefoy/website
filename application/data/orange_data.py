import sqlite3
import pandas as pd
import os
from config import basedir
import numpy as np


db_path = os.path.join(basedir, 'data/biocodex.db')

cnx = sqlite3.connect(db_path)

selection = [
    'lo_type', 'lo_title', 'supplier',
    'lo_id', 'lo_description', 'parent_subject', 'subject', 'active_status', 'detected_lang'
]

df = pd.read_sql_query(f"SELECT {', '.join(selection)} FROM learning_objects_table", cnx)

fname = os.path.join(basedir, 'data/csv/D_tfidf_2021_04_24.csv')

dtf = pd.read_csv(fname, sep=';')
dtf['active_status'] = np.where(dtf['active_status'] == 0, "inactif", "actif")
