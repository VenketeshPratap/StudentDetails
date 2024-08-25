import sqlite3

# Connect to the database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create the students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        total_marks INTEGER NOT NULL
    )
''')

# Insert sample data into the students table
students = [
    ('John Doe', 85),
    ('Jane Smith', 92),
    ('Alice Johnson', 78),
    ('Bob Brown', 88),
    ('Charlie Davis', 93),
    ('S Smith', 85),
    ('Mickle Clark', 92),
    ('Flaming', 78),
    ('Jack Sparrow', 88),
    ('Robert Dw jr', 93)
]

cursor.executemany('INSERT INTO students (name, total_marks) VALUES (?, ?)', students)

# Commit and close
conn.commit()
conn.close()
