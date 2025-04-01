#step1a(bash)
pip install openai

#step1b(python)
import openai

#step2(python  )
import sqlite3
import openai
import os

# OpenAI API Key (Set your own key)
openai.api_key = "your-api-key"

def get_table_schema(conn):
    """ Retrieves schema information for all tables in the database. """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = ""
    for table in tables:
        table_name = table[0]
        schema_info += f"\nTable: {table_name}\n"
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            schema_info += f" - {col[1]} ({col[2]})\n"
    
    return schema_info

def generate_sql_query(user_request, schema_info):
    """ Uses OpenAI to generate an SQL query based on user input and table schema. """
    prompt = f"""
    You are an expert SQL assistant. Based on the following table schema, generate an SQL query for the user's request.

    Schema:
    {schema_info}

    User Request:
    "{user_request}"

    SQL Query:
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a SQL expert."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"].strip()

def chat_assistant():
    """ Interactive chatbot for SQL queries with LLM support. """
    db_name = "database.db"
    conn = sqlite3.connect(db_name)

    print("\n🤖 Welcome to the AI-Powered SQLite Assistant!")
    print("You can:")
    print(" - 📂 Load a CSV file (type: load)")
    print(" - 🔍 Ask a question in plain English (type: ask)")
    print(" - 📝 Run a SQL query manually (type: query)")
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

        elif command == "ask":
            user_request = input("🔍 What would you like to know? ").strip()
            schema_info = get_table_schema(conn)
            sql_query = generate_sql_query(user_request, schema_info)
            
            print(f"\n🤖 AI-Generated SQL Query:\n{sql_query}\n")
            run_query(conn, sql_query)

        elif command == "exit":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid command. Try again.")

    conn.close()

# Start the assistant
chat_assistant()
