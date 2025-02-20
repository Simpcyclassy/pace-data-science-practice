import os
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin
from utils.create_directories import default_path, setup_logging, relative_path

# Use Airflow's logging system
log = LoggingMixin().log

def combine_extracted_files():
    """Combines extracted files from vehicle, toll plaza, and payment data into a single dataset."""
    setup_logging()

    processed_data_dir = os.getenv('PROCESSED_DATA_DIR', default_path('processed_data'))

    # Define file paths
    vehicle_data_file = os.path.join(processed_data_dir, "csv_d.csv")
    tollplaza_data_file = os.path.join(processed_data_dir, "tsv_d.csv")
    payment_data_file = os.path.join(processed_data_dir, "fixed_width_d.csv")
    combined_file = os.path.join(processed_data_dir, "combined_data.csv")

    # Check if all files exist
    missing_files = [f for f in [vehicle_data_file, tollplaza_data_file, payment_data_file] if not os.path.exists(f)]
    if missing_files:
        log.error(f"❌ Combination failed: Missing files - {', '.join([relative_path(f) for f in missing_files])}")
        return

    log.info(f"📂 Loading extracted files for combination...")

    try:
        # Load extracted files
        df_vehicle = pd.read_csv(vehicle_data_file)
        df_tollplaza = pd.read_csv(tollplaza_data_file)
        df_payment = pd.read_csv(payment_data_file)

        # Ensure all files have the same number of rows before combining
        min_rows = min(len(df_vehicle), len(df_tollplaza), len(df_payment))
        df_vehicle = df_vehicle.iloc[:min_rows]
        df_tollplaza = df_tollplaza.iloc[:min_rows]
        df_payment = df_payment.iloc[:min_rows]

        # Concatenate side-by-side (column-wise)
        combined_df = pd.concat([df_vehicle, df_tollplaza, df_payment], axis=1)

        # Save the combined dataset
        combined_df.to_csv(combined_file, index=False)

        log.info(f"✅ Combination successful! Combined data saved to {relative_path(combined_file)}")
        log.info(f"📊 Final dataset: {combined_df.shape[0]} rows, {combined_df.shape[1]} columns")

    except Exception as e:
        log.error(f"❌ Combination failed: {str(e)}")
        raise

# Run function if executed directly
if __name__ == "__main__":
    combine_extracted_files()
