import sys
import os
import psycopg2
import json

# Add parent directory to sys.path to allow importing setup_directories.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from setup_directories import setup_logging, FILES

# Set up logging
log = setup_logging("db_setup")

# Load database configuration
with open(FILES["DB_CONFIG"], "r") as config_file:
    db_config = json.load(config_file)

def create_database():
    """Ensures the PostgreSQL database and table exist, creating them if necessary."""

    try:
        # Step 1: Connect to default 'postgres' database to check/create 'weather_db'
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"]
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_config['dbname']}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {db_config['dbname']}")
            log.info(f"✅ Database '{db_config['dbname']}' created successfully.")
        else:
            log.info(f"✅ Database '{db_config['dbname']}' already exists.")

        cursor.close()
        conn.close()

        # Step 2: Connect to 'weather_db' and create table in 'public' schema
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Explicitly set schema to public before table creation
        cursor.execute("SET search_path TO public;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT NOT NULL,
                temperature INT,
                wind_speed INT,
                humidity INT,
                timestamp TIMESTAMP,
                received_at TIMESTAMP
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()

        log.info(f"✅ Database '{db_config['dbname']}' and table weather_data setup complete..")

    except Exception as e:
        log.error(f"❌ Database setup failed: {str(e)}")

if __name__ == "__main__":
    create_database()
