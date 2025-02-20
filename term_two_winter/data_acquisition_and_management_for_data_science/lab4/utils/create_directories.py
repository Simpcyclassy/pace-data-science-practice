import logging
import os

from airflow.utils.log.logging_mixin import LoggingMixin

# Use Airflow's logging system
log = LoggingMixin().log

def default_path(path):
    """Returns the default path for the ETL pipeline."""
    base_path = os.getenv(
        'BASE_PATH',
        "/Users/chiomaonyekpere/Documents/PACE/data-science-python-practice/term_two_winter/data_acquisition_and_management_for_data_science/lab4"
    )
    return os.path.join(base_path, path)

def relative_path(full_path):
    """Returns the relative path from BASE_PATH for cleaner logging."""
    base_path = default_path("")  # Get BASE_PATH
    return os.path.relpath(full_path, base_path) if full_path.startswith(base_path) else full_path

def setup_logging():
    """Configures logging to write both to Airflow logs and a persistent log file."""
    log_file_path = os.path.join(default_path('logs'), 'etl.log')

    # Prevent duplicate handlers
    if not any(isinstance(handler, logging.FileHandler) for handler in log.handlers):
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler.setFormatter(file_formatter)
        log.addHandler(file_handler)

    log.info(f"Logging to: {relative_path(log_file_path)}")

def create_directories():
    """Dynamically creates required directories for the ETL pipeline and logs the process."""
    directories = {
        'RAW_DATA_DIR': os.getenv('RAW_DATA_DIR', default_path('raw_data')),
        'PROCESSED_DATA_DIR': os.getenv('PROCESSED_DATA_DIR', default_path('processed_data')),
        'LOG_DIR': os.getenv('LOG_DIR', default_path('logs')),
        'TEMP_DIR': os.getenv('TEMP_DIR', default_path('temp'))
    }

    # Ensure log directory exists
    os.makedirs(directories['LOG_DIR'], exist_ok=True)

    setup_logging()

    for name, path in directories.items():
        try:
            os.makedirs(path, exist_ok=True)
            if os.path.exists(path):
                log.info(f"✅ Successfully created: {relative_path(path)}/ ({name})")
            else:
                log.error(f"❌ Failed to create: {relative_path(path)}/")
        except Exception as e:
            log.error(f"❌ Error creating {relative_path(path)}/: {str(e)}")

    log.info("✅ Directory structure set up successfully!")

# Run the function if executed directly
if __name__ == "__main__":
    create_directories()
