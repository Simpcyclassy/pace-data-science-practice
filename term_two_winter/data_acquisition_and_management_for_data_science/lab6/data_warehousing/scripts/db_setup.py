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
    """Creates the PostgreSQL database 'bill_DWH' if it does not exist."""
    try:
        # Connect to the default 'postgres' database to check/create 'bill_DWH'
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
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'bill_DWH'")
        if cursor.fetchone():
            log.info("✅ Database 'bill_DWH' already exists.")
        else:
            cursor.execute("CREATE DATABASE bill_DWH")
            log.info("✅ Database 'bill_DWH' created successfully.")

        cursor.close()
        conn.close()

    except Exception as e:
        log.error(f"❌ Database setup failed: {str(e)}")

if __name__ == "__main__":
    create_database()
