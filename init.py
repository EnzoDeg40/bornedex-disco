import sqlite3

conn = sqlite3.connect('bornes.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bornes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        lon REAL NOT NULL,
        lat REAL NOT NULL,
        ville TEXT NOT NULL,
        is_valid BOOLEAN NOT NULL DEFAULT 0
    )
''')

conn.commit()
conn.close()
