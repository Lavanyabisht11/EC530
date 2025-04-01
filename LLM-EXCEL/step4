#step1(python)
import sqlite3
import pandas as pd
import os

def list_tables(conn):
    """ Lists all tables in the database. """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        print("\n📋 Available Tables:")
        for table in tables:
            print(f" - {table[0]}")
    else:
        print("\n⚠️ No tables found.")

def run_query(conn, query):
    """ Executes a SQL query and displays results. """
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No results found.")
        else:
            conn.commit()
            print("✅ Query executed successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")

def chat_assistant():
    """ A simple CLI chatbot to interact with SQLite. """
    db_name = "database.db"
    conn = sqlite3.connect(db_name)

    print("\n🤖 Welcome to the SQLite Assistant!")
    print("You can:")
    print(" - 📂 Load a CSV file (type: load)")
    print(" - 📝 Run a SQL query (type: query)")
    print(" - 📋 List tables (type: tables)")
    print(" - ❌ Exit (type: exit)")

    while True:
        command = input("\n🔹 Enter command: ").strip().lower()

        if command == "load":
            csv_file = input("📂 Enter CSV file name: ").strip()
            if os.path.exists(csv_file):
                infer_and_create_table(csv_file, db_name)
            else:
                print("❌ File not found!")

        elif command == "query":
            query = input("📝 Enter SQL query: ").strip()
            run_query(conn, query)

        elif command == "tables":
            list_tables(conn)

        elif command == "exit":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid command. Try again.")

    conn.close()

# Start the assistant
chat_assistant()
