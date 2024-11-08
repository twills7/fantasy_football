import sqlite3

# Connect to the database
connection = sqlite3.connect("./data_management/player_base.db")
cursor = connection.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price_2024 INTEGER,
    price_2023 INTEGER,
    points_2024 INTEGER,
    team TEXT
    position TEXT
)
''')
