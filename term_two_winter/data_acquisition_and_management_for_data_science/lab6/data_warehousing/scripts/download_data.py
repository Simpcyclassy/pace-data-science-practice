import os
import requests
import tarfile
import sys

# Add parent directory to sys.path to allow importing setup_directories.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from setup_directories import setup_logging, DIRECTORIES, relative_path

# Define the dataset URL
DATA_URL = "https://elasticbeanstalk-us-east-2-340729127361.s3.us-east-2.amazonaws.com/billing-datawarehouse.tgz"

# Extract filename from URL
TGZ_FILENAME = os.path.basename(DATA_URL)

# Initialize logging
log = setup_logging("download")

# Define paths
TEMP_DIR = DIRECTORIES["TEMP_DIR"]
TGZ_FILE_PATH = os.path.join(TEMP_DIR, TGZ_FILENAME)
EXTRACT_PATH = DIRECTORIES["SQL_DIR"]  # Extract SQL files here

def download_tgz():
    """Downloads the .tgz file from the specified URL and saves it locally without renaming."""
    log.info(f"📥 Downloading data from {DATA_URL}...")

    try:
        response = requests.get(DATA_URL, stream=True)
        response.raise_for_status()  # Raise error if download fails

        with open(TGZ_FILE_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        log.info(f"✅ Data successfully downloaded to {relative_path(TGZ_FILE_PATH)}")
        return True

    except requests.exceptions.RequestException as e:
        log.error(f"❌ Failed to download data: {e}")
        return False

def extract_tgz():
    """Extracts the downloaded .tgz file into the sql_queries/ directory."""
    log.info(f"📂 Extracting files from {relative_path(TGZ_FILE_PATH)} to {relative_path(EXTRACT_PATH)}...")

    try:
        with tarfile.open(TGZ_FILE_PATH, "r:gz") as tar:
            tar.extractall(EXTRACT_PATH)

        log.info(f"✅ Extraction complete. Files saved to {relative_path(EXTRACT_PATH)}")
        return True

    except tarfile.TarError as e:
        log.error(f"❌ Failed to extract .tgz file: {e}")
        return False

if __name__ == "__main__":
    os.makedirs(TEMP_DIR, exist_ok=True)

    if download_tgz():
        extract_tgz()
