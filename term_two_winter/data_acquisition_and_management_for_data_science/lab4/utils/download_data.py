import os
import requests
from airflow.utils.log.logging_mixin import LoggingMixin
from utils.create_directories import default_path, setup_logging, relative_path

# Use Airflow's logging system
log = LoggingMixin().log

def download_traffic_data():
    """Downloads traffic data and saves it to the temp directory."""
    setup_logging()

    temp_dir = os.getenv('TEMP_DIR', default_path('temp'))
    os.makedirs(temp_dir, exist_ok=True)

    # Define the dataset URL
    data_url = "https://elasticbeanstalk-us-east-2-340729127361.s3.us-east-2.amazonaws.com/trafficdata.tgz"
    file_name = data_url.split("/")[-1]
    output_file = os.path.join(temp_dir, file_name)

    log.info(f"📥 Starting download from {data_url}...")

    try:
        response = requests.get(data_url, stream=True, timeout=60)
        response.raise_for_status()

        with open(output_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        log.info(f"✅ Download successful: {relative_path(output_file)}")

    except requests.exceptions.Timeout:
        log.error("❌ Download failed due to timeout!")
    except requests.exceptions.RequestException as e:
        log.error(f"❌ Download failed: {str(e)}")
        raise

if __name__ == "__main__":
    download_traffic_data()
