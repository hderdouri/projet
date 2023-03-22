import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

c.execute('''CREATE TABLE items
             (id INTEGER PRIMARY KEY, name TEXT, description TEXT, created_at TIMESTAMP)''')

conn.commit()
conn.close()
