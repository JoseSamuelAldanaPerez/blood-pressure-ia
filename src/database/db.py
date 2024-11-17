import sqlite3
from flask import g

DATABASE = 'src/database/database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    tables = [
        '''
          CREATE TABLE IF NOT EXISTS blood_pressure (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              systolic REAL NOT NULL,
              diastolic REAL NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
        '''
    ]
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        for table in tables:
            cursor.execute(table)


def close_connection(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
