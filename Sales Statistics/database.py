import sqlite3
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS sales (
id INTEGER PRIMARY KEY AUTOINCREMENT,
product TEXT NOT NULL,
category TEXT NOT NULL,
amount INTEGER NOT NULL,
date TEXT NOT NULL
)
''')

c.execute('''
INSERT INTO sales (product, category, amount, date)
VALUES (?, ?, ?, ?)
''', ('iPhone', 'electronics', 1000, '2023-11-26'))
c.execute('''
INSERT INTO sales (product, category, amount, date)
VALUES (?, ?, ?, ?)
''', ('MacBook', 'electronics', 2000, '2023-11-25'))
c.execute('''
INSERT INTO sales (product, category, amount, date)
VALUES (?, ?, ?, ?)
''', ('Coffee', 'food', 5, '2023-11-26'))
c.execute('''
INSERT INTO sales (product, category, amount, date)
VALUES (?, ?, ?, ?)
''', ('iPad', 'electronics', 800, '2023-11-25'))
c.execute('''
INSERT INTO sales (product, category, amount, date)
VALUES (?, ?, ?, ?)
''', ('Book', 'education', 20, '2023-11-24'))

conn.commit()
conn.close()