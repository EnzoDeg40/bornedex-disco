import sqlite3
import json

conn = sqlite3.connect('bornes.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM bornes')

rows = cursor.fetchall()

data = []
for row in rows:
    data.append(dict(zip([column[0] for column in cursor.description], row)))

with open('bornes.json', 'w') as file:
    json.dump(data, file)

conn.close()