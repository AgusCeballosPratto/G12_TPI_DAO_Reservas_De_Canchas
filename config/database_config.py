import sqlite3

def get_connection(db_name="reservasdecanchas.db"):
    conn = sqlite3.connect(db_name)
    return conn
