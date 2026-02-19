import os
import sys
import sqlite3
import shutil

def get_database_path():
    base_folder = r"C:\ProgramData\ClubGPLStoc"
    os.makedirs(base_folder, exist_ok=True)
    db_path = os.path.join(base_folder, "StocClubGPL.db")

    if not os.path.exists(db_path):
        if getattr(sys, 'frozen', False):
            source_folder = sys._MEIPASS
        else:
            source_folder = os.path.dirname(os.path.abspath(__file__))
        source_db = os.path.join(source_folder, "StocClubGPL.db")
        if os.path.exists(source_db):
            shutil.copy(source_db, db_path)
    return db_path

def get_connection():
    db_path = get_database_path()
    return sqlite3.connect(db_path)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            IdProduct INTEGER PRIMARY KEY AUTOINCREMENT,
            Nume TEXT NOT NULL,
            Pret REAL NOT NULL,
            Cantitate INTEGER NOT NULL,
            Vandute INTEGER DEFAULT 0,
            Incasate REAL DEFAULT 0,
            Neincasate REAL DEFAULT 0,
            DataVanzare DATE DEFAULT CURRENT_DATE
        )
    """)
    conn.commit()
    conn.close()


def add_data_vanzare_column():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE Products ADD COLUMN DataVanzare DATE DEFAULT CURRENT_DATE")
        conn.commit()
    except sqlite3.OperationalError:
        # coloana există deja, nu face nimic
        pass
    conn.close()
