import os
import sqlite3
from config.settings import settings


def get_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection and ensure directories exist.
    """
    db_path = settings.DB_PATH
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
