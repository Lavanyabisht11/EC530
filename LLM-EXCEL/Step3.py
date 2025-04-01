#step1(python)

import sqlite3
import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(filename="error_log.txt", level=logging.ERROR, format="%(asctime)s - %(message)s")

def get_existing_schema(table_name, conn):
    """ Retrieves the schema of an existing table in SQLite. """
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1]: row[2] for row in cursor.fetchall()}  # Returns {column_name: column_type}

def infer_and_create_table(csv_file, db_name="database.db"):
    """
    Reads a CSV file, infers column names and data types,
    and dynamically creates a SQLite table with schema validation.
    """
    try:
        df = pd.read_csv(csv_file)
        table_name = os.path.splitext(os.path.basename(csv_file))[0]

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Check if table exists
        existing_schema = get_existing_schema(table_name, conn)

        if existing_schema:
            print(f"⚠️ Table '{table_name}' already exists. Choose an action:")
            print("[1] Overwrite")
            print("[2] Rename new table")
            print("[3] Skip")
            choice = input("Enter 1, 2, or 3: ")

            if choice == "1":
                print(f"Overwriting table '{table_name}'...")
                cursor.execute(f"DROP TABLE {table_name}")  # Delete existing table

            elif choice == "2":
                new_table_name = input("Enter new table name: ")
                table_name = new_table_name  # Rename table
                
            elif choice == "3":
                print(f"Skipping '{table_name}'.")
                conn.close()
                return
            else:
                print("Invalid choice. Skipping table creation.")
                conn.close()
                return

        # Define data type mapping
        type_mapping = {
            "int64": "INTEGER",
            "float64": "REAL",
            "object": "TEXT"
        }

        # Infer column names and data types
        columns = []
        for col, dtype in df.dtypes.items():
            sql_type = type_mapping.get(str(dtype), "TEXT")  # Default to TEXT
            columns.append(f"{col} {sql_type}")

        # Create the SQL statement
        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
        cursor.execute(create_table_query)

        # Insert data
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()

        print(f"✅ Table '{table_name}' created and data inserted.")

    except Exception as e:
        logging.error(f"Error processing {csv_file}: {e}")
        print(f"❌ Error occurred! Check 'error_log.txt' for details.")

# Example usage
infer_and_create_table("students.csv")
