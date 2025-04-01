#step1(python)
import sqlite3
import pandas as pd
import os

def infer_and_create_table(csv_file, db_name="database.db"):
    """
    Reads a CSV file, infers column names and data types, 
    and dynamically creates a SQLite table.
    """
    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Extract table name from the filename (without extension)
    table_name = os.path.splitext(os.path.basename(csv_file))[0]

    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

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
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"

    # Execute the query to create the table
    cursor.execute(create_table_query)

    # Insert data into the table
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    # Commit and close connection
    conn.commit()
    conn.close()

    print(f"Table '{table_name}' created and data inserted.")

  
      
