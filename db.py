import sqlite3
import os

os.makedirs('data', exist_ok=True)

conn = sqlite3.connect('data/users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    identificador TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT UNIQUE,
    senha TEXT NOT NULL
)
''')

conn.commit()
conn.close()
