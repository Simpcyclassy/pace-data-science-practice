#!/bin/bash

# Set the base directory relative to the script location
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)" # Moves up one level from scripts/

# Database connection details
DB_NAME="bill_dwh"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"

# Define correct paths
SQL_DIR="$BASE_DIR/sql_queries"
LOG_DIR="$BASE_DIR/logs"
LOG_FILE="$LOG_DIR/execution.log"

# Ensure logs directory exists
mkdir -p "$LOG_DIR"

# SQL Files
SCHEMA_FILE="$SQL_DIR/star-schema.sql"
DIM_CUSTOMER_FILE="$SQL_DIR/DimCustomer.sql"
DIM_MONTH_FILE="$SQL_DIR/DimMonth.sql"
FACT_BILLING_FILE="$SQL_DIR/FactBilling.sql"
VERIFY_FILE="$SQL_DIR/verify.sql"

# Function to log messages
log_message() {
    local message="$1"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$timestamp $message" | tee -a "$LOG_FILE"
}

# Function to execute an SQL file
execute_sql() {
    local sql_file="$1"
    local description="$2"

    if [[ ! -f "$sql_file" ]]; then
        log_message "❌ SQL file not found: $sql_file"
        return 1
    fi

    log_message "📄 Executing: $description ($sql_file)"
    
    PGPASSWORD="postgres" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -f "$sql_file" >> "$LOG_FILE" 2>&1
    
    if [[ $? -ne 0 ]]; then
        log_message "❌ Failed to execute: $description"
        return 1
    fi

    log_message "✅ Successfully executed: $description"
    return 0
}


# Main Execution Flow
log_message "🚀 Starting SQL Execution Process"

# Step 4: Create the schema
execute_sql "$SCHEMA_FILE" "Star Schema Creation"

# Step 5: Load Dimension Tables
execute_sql "$DIM_CUSTOMER_FILE" "DimCustomer Table Load"
execute_sql "$DIM_MONTH_FILE" "DimMonth Table Load"

# Step 6: Load Fact Table
execute_sql "$FACT_BILLING_FILE" "FactBilling Table Load"

# Step 7: Run Final Data Verification
execute_sql "$VERIFY_FILE" "Final Data Verification"

log_message "✅ Data warehouse setup and data load completed successfully!"
