import sqlite3

connection = sqlite3.connect("shop.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    purchase_price REAL NOT NULL,
    sale_price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

connection.commit()
connection.close()

print("Database created successfully!")