import os
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin
from utils.create_directories import default_path, setup_logging, relative_path

# Use Airflow's logging system
log = LoggingMixin().log

def transform_combined_data():
    """Transforms 'Vehicle type' column to uppercase in the combined data file."""
    setup_logging()

    processed_data_dir = os.getenv('PROCESSED_DATA_DIR', default_path('processed_data'))

    # Ensure processed_data directory exists
    os.makedirs(processed_data_dir, exist_ok=True)

    # Define input and output file paths
    input_file = os.path.join(processed_data_dir, "combined_data.csv")
    output_file = os.path.join(processed_data_dir, "combined_data_transformed.csv")

    # Check if the combined file exists
    if not os.path.exists(input_file):
        log.error(f"❌ Transformation failed: File {relative_path(input_file)} not found!")
        return

    log.info(f"🔄 Transforming 'Vehicle type' column in {relative_path(input_file)}...")

    try:
        # Read the dataset (comma-separated)
        df = pd.read_csv(input_file)

        # Convert 'Vehicle type' column (column index 3) to uppercase
        df.iloc[:, 3] = df.iloc[:, 3].str.upper()

        # Save the transformed data
        df.to_csv(output_file, index=False)

        # Log transformation results
        row_count, col_count = df.shape
        log.info(f"✅ Transformation successful! Transformed data saved to {relative_path(output_file)}")
        log.info(f"📊 Transformed dataset contains {row_count} rows and {col_count} columns.")

    except Exception as e:
        log.error(f"❌ Transformation failed: {str(e)}")
        raise

# Run function if executed directly
if __name__ == "__main__":
    transform_combined_data()
