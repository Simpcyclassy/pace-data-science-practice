import os
import psycopg2
import sys
import json

# Add parent directory to sys.path to allow importing setup_directories.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from setup_directories import setup_logging, FILES, DIRECTORIES, relative_path

# Initialize logging
log = setup_logging("execution")

# Load database configuration
with open(FILES["DB_CONFIG"], "r") as config_file:
    db_config = json.load(config_file)

# Define SQL file paths
SCHEMA_FILE = os.path.join(DIRECTORIES["SQL_DIR"], "star-schema.sql")
DIM_CUSTOMER_FILE = os.path.join(DIRECTORIES["SQL_DIR"], "DimCustomer.sql")
DIM_MONTH_FILE = os.path.join(DIRECTORIES["SQL_DIR"], "DimMonth.sql")
FACT_BILLING_FILE = os.path.join(DIRECTORIES["SQL_DIR"], "FactBilling.sql")
VERIFY_FILE = os.path.join(DIRECTORIES["SQL_DIR"], "verify.sql")

SQL_FILES = {
    "Star Schema": SCHEMA_FILE,
    "DimCustomer": DIM_CUSTOMER_FILE,
    "DimMonth": DIM_MONTH_FILE,
    "FactBilling": FACT_BILLING_FILE,
    "Verify Data": VERIFY_FILE
}

def connect_to_db():
    """Establishes a connection to the PostgreSQL database."""
    try:
        log.info(f"🔗 Connecting to database: {db_config['dbname']} on {db_config['host']}:{db_config['port']}")
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        log.error(f"❌ Database connection failed: {e}")
        return None

def execute_sql_file(file_path, description):
    """Executes the SQL script from the specified file."""
    if not os.path.exists(file_path):
        log.error(f"❌ SQL file not found: {relative_path(file_path)}")
        return False

    log.info(f"📄 Executing {description}: {relative_path(file_path)}")

    try:
        conn = connect_to_db()
        if not conn:
            return False

        cursor = conn.cursor()

        with open(file_path, "r") as sql_file:
            sql_commands = sql_file.read()
            cursor.execute(sql_commands)

        conn.commit()
        cursor.close()
        conn.close()
        
        log.info(f"✅ Successfully executed: {relative_path(file_path)}")
        return True

    except Exception as e:
        log.error(f"❌ SQL execution failed for {description}: {e}")
        return False

def verify_table_data(table_name):
    """Verifies if data exists in the given table with case-sensitive handling."""
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()

    log.info(f"🔍 Verifying data in table: \"{table_name}\"")

    try:
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}";')  # Use double quotes
        count = cursor.fetchone()[0]

        if count > 0:
            log.info(f"✅ Table \"{table_name}\" contains {count} records.")
        else:
            log.warning(f"⚠️ Table \"{table_name}\" is empty!")

    except Exception as e:
        log.error(f"❌ Failed to verify table \"{table_name}\": {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Step 4: Create the schema
    if execute_sql_file(SQL_FILES["Star Schema"], "Star Schema Creation"):
        verify_table_data("dimcustomer")  # Check if schema is created

    # Step 5: Load Dimension Tables
    if execute_sql_file(SQL_FILES["DimCustomer"], "DimCustomer Table Load"):
        verify_table_data("dimcustomer")

    if execute_sql_file(SQL_FILES["DimMonth"], "DimMonth Table Load"):
        verify_table_data("dimmonth")

    # Step 6: Load Fact Table
    if execute_sql_file(SQL_FILES["FactBilling"], "FactBilling Table Load"):
        verify_table_data("factbilling")

    # Step 7: Run Final Data Verification
    if execute_sql_file(SQL_FILES["Verify Data"], "Final Data Verification"):
        log.info("✅ Data verification completed successfully!")
