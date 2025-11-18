import sqlite3

# Connect to a database (or create one)
conn = sqlite3.connect('mydatabase.db')

# 2️⃣ Create a cursor object
cursor = conn.cursor()

# 3️⃣ Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
''')

# 4️⃣ Insert data
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Rajneesh', 30))

# 5️⃣ Commit changes
conn.commit()

# 6️⃣ Fetch data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 7️⃣ Close connection
conn.close()
