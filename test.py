import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# real is just a decimal point
create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
users = [(1, "jose", "asdf"), (2, "rolf", "asdf"), (3, "anne", "xyz")]
cursor.executemany(insert_query, users)

"""
select_query = "SELECT * FROM users"
cursor.execute(select_query)
for row in cursor.execute(select_query):
    print(row)
"""

connection.commit()
connection.close()
