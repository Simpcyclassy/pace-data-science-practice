import sys
import os
import json
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime

# Add parent directory to sys.path to allow importing setup_directories.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from setup_directories import setup_logging, FILES

# Set up logging for consumer
log = setup_logging("consumer")

# Load database configuration
with open(FILES["DB_CONFIG"], "r") as config_file:
    db_config = json.load(config_file)

# Kafka Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "weather-data")

def connect_to_db():
    """Establishes connection to the PostgreSQL database."""
    try:
        log.info(f"Connecting to database: {db_config['dbname']} on {db_config['host']}:{db_config['port']}")
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        log.error(f"❌ Database connection failed: {str(e)}")
        return None

def log_existing_tables(cursor):
    """Logs the existing tables in the database."""
    try:
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]
        log.info(f"📋 Existing tables in database: {table_list}")
    except Exception as e:
        log.error(f"❌ Failed to fetch table list: {str(e)}")

def consume_weather_data():
    """Consumes weather data from Kafka and stores it in PostgreSQL."""
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        log.info(f"✅ Connected to Kafka topic: {KAFKA_TOPIC}")

        conn = connect_to_db()
        if not conn:
            log.error("❌ Exiting due to database connection failure.")
            return
        
        cursor = conn.cursor()

        # Log existing tables before inserting data
        log_existing_tables(cursor)

        # ✅ Explicitly set schema to public before performing inserts
        cursor.execute("SET search_path TO public;")

        row_count = 0  # Counter for inserted rows

        for message in consumer:
            weather_data = message.value  # Extract JSON data
            received_at = datetime.now()  # Append received timestamp

            # Log received data
            log.info(f"📥 Received: {weather_data}")

            # Insert data into PostgreSQL
            try:
                timestamp = datetime.fromisoformat(weather_data["timestamp"])  # Fix timestamp parsing

                cursor.execute("""
                    INSERT INTO public.weather_data (city, temperature, wind_speed, humidity, timestamp, received_at)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    weather_data["city"],
                    weather_data["temperature"],
                    weather_data["wind_speed"],
                    weather_data["humidity"],
                    timestamp,
                    received_at
                ))

                conn.commit()
                row_count += 1  # Increment row count

                # Log the insertion with the number of rows inserted
                log.info(f"✅ Inserted {row_count} row(s) into database.")

            except Exception as e:
                log.error(f"❌ Failed to insert data into database: {str(e)}")
                conn.rollback()

        cursor.close()
        conn.close()

    except Exception as e:
        log.error(f"❌ Kafka Consumer error: {str(e)}")

if __name__ == "__main__":
    consume_weather_data()
