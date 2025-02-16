import psycopg2
import os
import sys
from datetime import datetime

# Define database connection parameters
db_name = os.getenv('DB_NAME', 'covid_db')
db_user = os.getenv('PSQL_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'postgres')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')

# Define input file
transformed_data = "transformed_covid_data.csv"

conn = None
cursor = None

try:
    # Connect to PostgreSQL default database to check/create covid_db
    temp_conn = psycopg2.connect(
        dbname="postgres", user=db_user, password=db_password, host=db_host, port=db_port
    )
    temp_conn.autocommit = True
    temp_cursor = temp_conn.cursor()

    # Create the database if it doesn't exist
    temp_cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    if not temp_cursor.fetchone():
        temp_cursor.execute(f"CREATE DATABASE {db_name}")

    temp_cursor.close()
    temp_conn.close()

    # Now, connect to the actual database
    conn = psycopg2.connect(
        dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        SET search_path TO public;
        CREATE TABLE IF NOT EXISTS COVID (
            iso_code VARCHAR(10),
            continent VARCHAR(50),
            date DATE,
            total_cases BIGINT
        );
    """)

    # Load data into the table
    cursor.execute("DELETE FROM COVID;")
    with open(transformed_data, 'r') as file:
        cursor.copy_expert("COPY COVID FROM STDIN WITH CSV HEADER", file)

    # Check row count after insertion
    cursor.execute("SELECT COUNT(*) FROM COVID;")
    after_insert = cursor.fetchone()[0]
    rows_inserted = after_insert

    conn.commit()
    print(f"Data successfully loaded. {rows_inserted} rows inserted into {db_name}. Database now has {after_insert} rows.")

    # Log the inserted row count

    with open("ETL_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: Data successfully loaded. {rows_inserted} rows inserted. Database now has {after_insert} rows.\n")
    
    conn.commit()
    print("Data successfully loaded into PostgreSQL.")

except psycopg2.OperationalError as e:
    print("Database connection error:", e)
    sys.exit(1)
except Exception as e:
    print("Error loading data:", e)
    sys.exit(1)
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()