import os
import logging
from datetime import datetime

# Get the base directory dynamically (ensures it runs correctly from any location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Retrieve directory paths from environment variables with fallback defaults
DIRECTORIES = {
    "SCRIPTS_DIR": os.getenv("SCRIPTS_DIR", os.path.join(BASE_DIR, "kafka_pipeline/scripts")),
    "LOG_DIR": os.getenv("LOG_DIR", os.path.join(BASE_DIR, "kafka_pipeline/logs")),
    "CONFIG_DIR": os.getenv("CONFIG_DIR", os.path.join(BASE_DIR, "kafka_pipeline/config")),
    "DATA_DIR": os.getenv("DATA_DIR", os.path.join(BASE_DIR, "kafka_pipeline/data")),
}

FILES = {
    "PRODUCER_SCRIPT": os.path.join(DIRECTORIES["SCRIPTS_DIR"], "producer.py"),
    "CONSUMER_SCRIPT": os.path.join(DIRECTORIES["SCRIPTS_DIR"], "consumer.py"),
    "DB_SETUP_SCRIPT": os.path.join(DIRECTORIES["SCRIPTS_DIR"], "db_setup.py"),
    "PRODUCER_LOG": os.path.join(DIRECTORIES["LOG_DIR"], "producer.log"),
    "CONSUMER_LOG": os.path.join(DIRECTORIES["LOG_DIR"], "consumer.log"),
    "DB_CONFIG": os.path.join(DIRECTORIES["CONFIG_DIR"], "db_config.json"),
    "SAMPLE_DATA": os.path.join(DIRECTORIES["DATA_DIR"], "weather_data_sample.txt"),
}

# Ensure log directory exists before configuring logging
os.makedirs(DIRECTORIES["LOG_DIR"], exist_ok=True)

def relative_path(full_path):
    """Converts full file path to a relative path for cleaner logging."""
    return os.path.relpath(full_path, BASE_DIR)

def setup_logging(log_name="general"):
    """Configures logging with timestamps and saves logs to a specified log file."""
    log_file = os.path.join(DIRECTORIES["LOG_DIR"], f"{log_name}.log")
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    
    logger = logging.getLogger(log_name)
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger

def log_message(message, level="info", log_name="setup"):
    """Logs message with timestamp to both console and file."""
    logger = setup_logging(log_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{timestamp} {message}"
    
    if level == "info":
        logger.info(formatted_message)
        print(f"✅ {formatted_message}")
    elif level == "error":
        logger.error(formatted_message)
        print(f"❌ {formatted_message}")

def create_directories():
    """Creates necessary directories for the Kafka data pipeline."""
    for name, path in DIRECTORIES.items():
        os.makedirs(path, exist_ok=True)
        log_message(f"Created directory: {relative_path(path)}", log_name="setup")

def create_files():
    """Creates necessary empty files if they don't exist."""
    for name, path in FILES.items():
        if not os.path.exists(path):
            with open(path, "w") as f:
                pass  # Create an empty file
            log_message(f"Created file: {relative_path(path)}", log_name="setup")

if __name__ == "__main__":
    create_directories()
    create_files()
    log_message("Kafka pipeline directories and files are set up successfully!", log_name="setup")
