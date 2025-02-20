import os
import tarfile
import logging
from airflow.utils.log.logging_mixin import LoggingMixin
from utils.create_directories import default_path, setup_logging, relative_path

# Use Airflow's logging system
log = LoggingMixin().log

def extract_traffic_data():
    """Extracts the traffic data archive from the temp directory into raw_data and logs extracted files."""
    setup_logging()

    temp_dir = os.getenv('TEMP_DIR', default_path('temp'))
    raw_data_dir = os.getenv('RAW_DATA_DIR', default_path('raw_data'))

    # Ensure the raw_data directory exists
    os.makedirs(raw_data_dir, exist_ok=True)

    # Locate the archive
    archive_path = os.path.join(temp_dir, "trafficdata.tgz")
    if not os.path.exists(archive_path):
        log.error(f"❌ Extraction failed: Archive {relative_path(archive_path)} not found!")
        return

    log.info(f"📦 Extracting {relative_path(archive_path)} into {relative_path(raw_data_dir)}...")

    extracted_files = []
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=raw_data_dir)
            extracted_files = tar.getnames()  # Get a list of extracted files

        log.info(f"✅ Extraction successful! Files extracted to: {relative_path(raw_data_dir)}")

        # Log the list of extracted files
        if extracted_files:
            log.info(f"📂 Extracted files: {', '.join(extracted_files)}")
        else:
            log.warning("⚠️ No files were extracted!")

    except Exception as e:
        log.error(f"❌ Extraction failed: {str(e)}")
        raise

# Run function if executed directly
if __name__ == "__main__":
    extract_traffic_data()
