import os
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin
from utils.create_directories import default_path, setup_logging, relative_path

# Use Airflow's logging system
log = LoggingMixin().log

def extract_tollplaza_data():
    """Extracts columns 5, 6, and 7 from tollplaza-data.tsv and saves as tsv_d.csv."""
    setup_logging()

    raw_data_dir = os.getenv('RAW_DATA_DIR', default_path('raw_data'))
    processed_data_dir = os.getenv('PROCESSED_DATA_DIR', default_path('processed_data'))

    # Ensure processed_data directory exists
    os.makedirs(processed_data_dir, exist_ok=True)

    # Locate the extracted TSV file
    file_path = os.path.join(raw_data_dir, "tollplaza-data.tsv")
    if not os.path.exists(file_path):
        log.error(f"❌ Extraction failed: File {relative_path(file_path)} not found!")
        return

    log.info(f"🔄 Extracting columns from {relative_path(file_path)}...")

    try:
        # Read the dataset as a TSV file
        df = pd.read_csv(file_path, sep="\t", header=None)

        # Select required columns (Python uses 0-based index)
        extracted_df = df.iloc[:, [4, 5, 6]].copy()

        # Rename columns
        extracted_df.columns = ["Number_of_Axles", "Tollplaza_ID", "Tollplaza_Code"]

        # Save the extracted data
        output_file = os.path.join(processed_data_dir, "tsv_d.csv")
        extracted_df.to_csv(output_file, index=False)

        log.info(f"✅ Extraction successful! Data saved to {relative_path(output_file)}")
        log.info(f"📊 Extracted Data Summary: {len(extracted_df)} rows, {len(extracted_df.columns)} columns")

    except Exception as e:
        log.error(f"❌ Extraction failed: {str(e)}")
        raise

# Run function if executed directly
if __name__ == "__main__":
    extract_tollplaza_data()
