import sqlite3

DB_NAME = "nso.db"

def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_name TEXT PRIMARY KEY,
            country TEXT,
            target_open TEXT,
            need_rgm INTEGER, need_argm INTEGER, need_sup INTEGER, need_tm INTEGER,
            hired_rgm INTEGER, hired_argm INTEGER, hired_sup INTEGER, hired_tm INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS hires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT,
            role TEXT,
            name TEXT,
            background TEXT,
            start_date TEXT
        )
    """)
    conn.commit()
    conn.close()


def store_exists(store_name):
    conn = get_conn()
    row = conn.execute(
        "SELECT 1 FROM stores WHERE store_name = ?", (store_name,)
    ).fetchone()
    conn.close()
    return row is not None

def add_store(store_name, country, target_open,
              need_rgm, need_argm, need_sup, need_tm,
              hired_rgm, hired_argm, hired_sup, hired_tm):
    conn = get_conn()
    conn.execute(
        """INSERT INTO stores
           (store_name, country, target_open,
            need_rgm, need_argm, need_sup, need_tm,
            hired_rgm, hired_argm, hired_sup, hired_tm)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (store_name, country, str(target_open),
         need_rgm, need_argm, need_sup, need_tm,
         hired_rgm, hired_argm, hired_sup, hired_tm),
    )
    conn.commit()
    conn.close()


def add_hire(store_name, role, name, background, start_date):
    conn = get_conn()
    conn.execute(
        """INSERT INTO hires (store_name, role, name, background, start_date)
           VALUES (?, ?, ?, ?, ?)""",
        (store_name, role, name, background,
         str(start_date) if start_date else None),
    )
    conn.commit()
    conn.close()