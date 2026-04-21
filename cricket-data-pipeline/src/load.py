import os
import sqlite3
import pandas as pd


DB_PATH = "data/processed/cricket_data.db"


def create_connection():
    os.makedirs("data/processed", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def load_to_sqlite(df, table_name, conn):
    df.to_sql(table_name, conn, if_exists="replace", index=False)
