import supabase
import sqlite3

# Replace with your Supabase project URL and access key
SUPABASE_URL = "https://ffdawaoqehifvpsqxsvj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmZGF3YW9xZWhpZnZwc3F4c3ZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQxMDcyMzUsImV4cCI6MjAyOTY4MzIzNX0.DN9f57p_iPqAllCzcRM9kh2xL1o4QPh0Z1o0z_PomBw"

# Replace with your SQLite3 database filename
SQLITE_DB_PATH = "data.db"


def create_supabase_client():
    """Creates a Supabase client instance."""
    return supabase.create_client(SUPABASE_URL, SUPABASE_KEY)


def extract_sqlite_data(table_name):
    """Extracts data from a specific table in the SQLite3 database.

    Args:
        table_name: The name of the table to extract data from.

    Returns:
        A list of rows, where each row is a list of values.
    """
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # Get table schema (adjust based on your table structure)
    schema = cursor.execute(f"PRAGMA table_info('{table_name}')").fetchall()

    # Get table data
    data = cursor.execute(f"SELECT * FROM {table_name}").fetchall()

    conn.close()
    return schema, data


def import_data_to_supabase(table_name, schema, data):
    """Imports data into a Supabase table.

    Args:
        table_name: The name of the Supabase table to import data into.
        schema: A list of tuples representing the column names and types.
        data: A list of rows, where each row is a list of values.
    """
    supabase_client = create_supabase_client()

    # Create Supabase table if it doesn't exist (adjust column types as needed)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join([f"{col} {type}" for col, type in schema])}
    );
    """
    _, error = supabase_client.execute(create_table_query)

    if error:
        print(f"Error creating table {table_name}: {error}")
        return

    # Insert data into the Supabase table
    insert_statements = []
    for row in data:
        insert_statement = f"INSERT INTO {table_name} ({', '.join(['?' for _ in schema])}) VALUES ({', '.join(['%s' for _ in row])})"
        insert_statements.append(insert_statement)

    _, error = supabase_client.multiple_insert(table_name, insert_statements)

    if error:
        print(f"Error importing data into table {table_name}: {error}")


if __name__ == "__main__":
    # List of tables you want to migrate (modify accordingly)
    tables_to_migrate = ["your_table_name1", "your_table_name2"]

    for table in tables_to_migrate:
        schema, data = extract_sqlite_data(table)
        import_data_to_supabase(table, schema, data)

    print("Data migration completed (if no errors were reported).")

