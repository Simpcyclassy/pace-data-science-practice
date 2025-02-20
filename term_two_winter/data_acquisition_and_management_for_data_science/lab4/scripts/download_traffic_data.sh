#!/bin/bash
# download_traffic_data.sh

# Set default BASE_PATH if not already defined
BASE_PATH="${BASE_PATH:-/Users/chiomaonyekpere/Documents/PACE/data-science-python-practice/term_two_winter/data_acquisition_and_management_for_data_science/lab4}"

# Set TEMP_DIR, falling back to BASE_PATH/temp if not provided
TEMP_DIR="${TEMP_DIR:-${BASE_PATH}/temp}"

# Create the temporary directory if it doesn't exist
mkdir -p "$TEMP_DIR"

# Define the dataset URL
DATA_URL="https://elasticbeanstalk-us-east-2-340729127361.s3.us-east-2.amazonaws.com/trafficdata.tgz"
FILE_NAME=$(basename "$DATA_URL")
OUTPUT_FILE="${TEMP_DIR}/${FILE_NAME}"

echo "📥 Starting download from ${DATA_URL}..."

# Download the file using curl with a 60-second timeout
if curl --fail --location --max-time 60 -o "$OUTPUT_FILE" "$DATA_URL"; then
    echo "✅ Download successful: ${OUTPUT_FILE}"
else
    echo "❌ Download failed!"
    exit 1
fi
