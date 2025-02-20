import os
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin
from utils.create_directories import default_path, setup_logging, relative_path

# Use Airflow's logging system
log = LoggingMixin().log

def extract_vehicle_data():
    """Extracts and transforms required columns from vehicle-data.csv and saves them as csv_d.csv."""
    setup_logging()

    raw_data_dir = os.getenv('RAW_DATA_DIR', default_path('raw_data'))
    processed_data_dir = os.getenv('PROCESSED_DATA_DIR', default_path('processed_data'))

    # Ensure processed_data directory exists
    os.makedirs(processed_data_dir, exist_ok=True)

    # Locate the extracted CSV file
    file_path = os.path.join(raw_data_dir, "vehicle-data.csv")  # Updated filename based on extraction
    if not os.path.exists(file_path):
        log.error(f"❌ Transformation failed: File {relative_path(file_path)} not found!")
        return

    log.info(f"🔄 Transforming data from {relative_path(file_path)}...")

    try:
        # Read the dataset (CSV does not have headers, so define them explicitly)
        df = pd.read_csv(file_path, header=None, names=['Rowid', 'Timestamp', 'Anonymized_Vehicle_Number', 'Vehicle_Type', 'Axles', 'Plate_Number'])

        # Convert timestamp to datetime format
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

        # Select only the required columns
        transformed_df = df[['Rowid', 'Timestamp', 'Anonymized_Vehicle_Number', 'Vehicle_Type']]

        # Save the transformed data as csv_d.csv
        output_file = os.path.join(processed_data_dir, "csv_d.csv")
        transformed_df.to_csv(output_file, index=False)

        # Log row and column count
        log.info(f"✅ Transformation successful! Transformed data saved to {relative_path(output_file)}")
        log.info(f"📊 Transformed dataset contains {transformed_df.shape[0]} rows and {transformed_df.shape[1]} columns.")

    except Exception as e:
        log.error(f"❌ Transformation failed: {str(e)}")
        raise

# Run function if executed directly
if __name__ == "__main__":
    extract_vehicle_data()
