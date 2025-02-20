import os
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin
from utils.create_directories import default_path, setup_logging, relative_path

# Use Airflow's logging system
log = LoggingMixin().log

def extract_payment_data():
    """Extracts Type of Payment Code and Vehicle Code from the fixed-width file."""
    setup_logging()

    raw_data_dir = os.getenv('RAW_DATA_DIR', default_path('raw_data'))
    processed_data_dir = os.getenv('PROCESSED_DATA_DIR', default_path('processed_data'))

    # Ensure processed_data directory exists
    os.makedirs(processed_data_dir, exist_ok=True)

    # Locate the fixed-width file
    file_path = os.path.join(raw_data_dir, "payment-data.txt")
    if not os.path.exists(file_path):
        log.error(f"❌ Extraction failed: File {relative_path(file_path)} not found!")
        return

    log.info(f"🔄 Extracting fixed-width columns from {relative_path(file_path)}...")

    try:
        # Define column positions based on fixed-width format (adjusted for zero-based indexing)
        col_specifications = [(54, 57), (58, 63)]  # Start-1 for Python indexing

        # Read fixed-width formatted file (no header)
        df = pd.read_fwf(file_path, colspecs=col_specifications, header=None)

        # Rename extracted columns
        df.columns = ["Type_of_Payment_Code", "Vehicle_Code"]

        # Save the extracted data
        output_file = os.path.join(processed_data_dir, "fixed_width_d.csv")
        df.to_csv(output_file, index=False)

        # Log the result
        log.info(f"✅ Extraction successful! Data saved to {relative_path(output_file)}")
        log.info(f"📊 Extracted Data Summary: {len(df)} rows, {len(df.columns)} columns")

    except Exception as e:
        log.error(f"❌ Extraction failed: {str(e)}")
        raise

# Run function if executed directly
if __name__ == "__main__":
    extract_payment_data()
