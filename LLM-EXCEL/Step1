#step1(bash)
pip install pandas sqlite3

#step2(python)
import sqlite3

# Connect to SQLite database (creates one if it doesn't exist)
conn = sqlite3.connect("database.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Manually create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        grade TEXT
    )
""")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Table 'students' created successfully.")

#step3a(csv)
id,name,age,grade
1,Alice,20,A
2,Bob,21,B
3,Charlie,19,A

#step3b(python)
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("students.csv")

print(df.head())  # Display the first few rows

#step4(python)
# Reconnect to the SQLite database
conn = sqlite3.connect("database.db")

# Use pandas to insert data into SQLite
df.to_sql("students", conn, if_exists="replace", index=False)

#step5(python)
conn.close()
print("Data inserted into 'students' table.")

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Fetch all rows from the students table
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)

conn.close()
