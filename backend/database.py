import sqlite3

def get_db_connection():
    conn = sqlite3.connect("download_info.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS win_prog(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                compatibility TEXT NOT NULL,
                rating REAL,
                url_download TEXT NOT NULL,
                url_image TEXT,
                additional_info TEXT,
                category TEXT
        );
""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lin_prog(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                compatibility TEXT NOT NULL,
                rating REAL,
                url_download TEXT NOT NULL,
                url_image TEXT,
                additional_info TEXT
        );
""")
    conn.commit()
    cursor.close()

create_table()