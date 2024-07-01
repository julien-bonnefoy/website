# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from compat import basestring
import pandas as pd
from sqlalchemy import create_engine
from application.extensions import db
import os
import pyodbc
from dotenv import load_dotenv

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class PkModel(Model):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' column named ``id``."""

    __abstract__ = True
    id = Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col( tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )



def connect_to_azure(basedir, env_file):
    load_dotenv(os.path.join(basedir, env_file))

    driver = os.environ.get("DRIVER")
    server = os.environ.get("SERVER")
    database = os.environ.get("DATABASE")
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    port = os.environ.get("PORT")

    connection_string = f'DRIVER={driver};PORT=1433;SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        conn = pyodbc.connect(connection_string)
        print("connected")
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"error: {sqlstate}")
    else:
        return conn


def dropping_table_query(table_name):
    query = f"DROP TABLE IF EXISTS  {table_name}"
    return query


def creating_table_query(table_name, column_name, column_dtype):
    query = f"CREATE TABLE {table_name} ({column_name} {column_dtype} IDENTITY (1,1) PRIMARY KEY, {column_name} {column_dtype}, {column_name} {column_dtype});"
    return query


def insertion_data__query(table_name, column_name_1, column_name_2, value_1, value_2):
    query = f"INSERT INTO {table_name} ({column_name_1}, {column_name_2}) VALUES (?, ?);", ({value_1}, {value_1})
    return query


def select_all_query(table_name):
    query = f"SELECT * FROM {table_name};"
    return query


def update_value_query(table_name, column_name_1, column_name_2, value_1, value_2):
    query = f"UPDATE {table_name}  SET {column_name_1} = ? WHERE {column_name_2} = ?;", ({value_1}, {value_2})
    return query


def delete_row_query(table_name, column_name, value):
    query = f"DELETE FROM {table_name} WHERE {column_name} = {value};"
    return query


def execute_sql_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    return None


def df_to_mysql(df, table_name, server, db, usr, pwd, port):
    engine = create_engine(f"mssql+pyodbc://{usr}:{pwd}@{server}:{port}/{db}?driver=ODBC+Driver+17+for+SQL+Server")

    # Insert whole DataFrame into MySQL
    df.to_sql(table_name, con=engine, if_exists='replace', chunksize=1000, index=False)

    return print(f'{len(df)} rows transferred to azure {db} on {server} server')


def mysql_to_df(table_name, server, db, usr, pwd, port):
    # create sqlalchemy engine
    engine = create_engine(f"mssql+pyodbc://{usr}:{pwd}@{server}:{port}/{db}?driver=ODBC+Driver+17+for+SQL+Server")

    # Insert whole DataFrame into MySQL
    df = pd.read_sql_table(table_name, con=engine)

    print(f'{len(df)} rows imported from azure {db} on {server} server')

    return df


def to_sqlalch_dtypes(df):
    type_dict = df.dtypes.to_dict()
    alch_types = {}
    for k, v in type_dict.items():
        print(v)
        if v == 'float64':
            alch_types[k] = 'Float'
        elif v == 'int64':
            alch_types[k] = 'Integer'
        elif v == 'bool':
            alch_types[k] = 'Boolean'
        elif v == 'datetime64':
            alch_types[k] = 'DateTime'
        else:
            alch_types[k] = 'Text'
    return alch_types
