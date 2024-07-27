import os
import sqlite3
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DATABASE_NAME = resource_path("permits.db")

def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS permits (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                permit_number TEXT NOT NULL UNIQUE,
                valid_until TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_permit(name: str, position: str, valid_until: str, file_path: str) -> str:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(permit_number) FROM permits')
        max_permit_number = cursor.fetchone()[0]
        new_permit_number = str(int(max_permit_number) + 1) if max_permit_number else "1024"
        cursor.execute('''
            INSERT INTO permits (name, position, permit_number, valid_until, file_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, position, new_permit_number, valid_until, file_path))
        conn.commit()
        return new_permit_number

def get_permits():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM permits')
        return cursor.fetchall()

def delete_permit(permit_id: int):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM permits WHERE id = ?', (permit_id,))
        conn.commit()

init_db()
