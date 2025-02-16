#!/bin/bash

# Extract Phase: Download dataset
DATA_URL="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
RAW_DATA="raw_owid_covid_data.csv"
TRANSFORMED_DATA="transformed_covid_data.csv"
LOG_FILE="ETL_log.txt"

# Log the start of the extraction process
echo "$(date): Starting data extraction..." >> $LOG_FILE

# Download the dataset (overwrite existing file to get the latest data)
curl -o $RAW_DATA $DATA_URL

# Verify if the file was downloaded successfully
if [[ -f "$RAW_DATA" ]]; then
    ROW_COUNT=$(($(wc -l < "$RAW_DATA") - 1))
COL_COUNT=$(head -1 "$RAW_DATA" | awk -F',' '{print NF}')
echo "$(date): Data extraction successful. Rows extracted: $ROW_COUNT, Columns extracted: $COL_COUNT" >> $LOG_FILE
else
    echo "$(date): Data extraction failed" >> $LOG_FILE
    exit 1
fi

# Transform Phase: Select specific columns
echo "$(date): Starting data transformation..." >> $LOG_FILE

# Select only required columns
cut -d',' -f1,2,4,5 $RAW_DATA > $TRANSFORMED_DATA

# Count the number of transformed rows (excluding header)
ROW_COUNT=$(($(wc -l < "$TRANSFORMED_DATA") - 1))

# Verify if transformation was successful
if [[ -f "$TRANSFORMED_DATA" ]]; then
    COL_COUNT=$(head -1 "$TRANSFORMED_DATA" | awk -F',' '{print NF}')
echo "$(date): Data transformation successful. Rows transformed: $ROW_COUNT, Columns retained: $COL_COUNT" >> $LOG_FILE
else
    echo "$(date): Data transformation failed" >> $LOG_FILE
    exit 1
fi


# Load Phase: Load transformed data into PostgreSQL
echo "$(date): Starting data load into PostgreSQL..." >> $LOG_FILE
python3 daily_covid_update.py

if [[ $? -eq 0 ]]; then
    echo "$(date): Data successfully loaded into PostgreSQL" >> $LOG_FILE
else
    echo "$(date): Data load failed" >> $LOG_FILE
fi