import sqlite3
import pandas as pd


def run_query(conn: sqlite3.Connection, query: str) -> pd.DataFrame:
    """
    Execute a SQL query and return a pandas DataFrame.
    """
    return pd.read_sql_query(query, conn)
