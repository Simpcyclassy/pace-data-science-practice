import sys
import os

# Add parent directory to sys.path to allow importing setup_directories.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from setup_directories import setup_logging

# Set up logging
log = setup_logging("producer")

# Kafka configuration
TOPIC_NAME = "weather-data"
BOOTSTRAP_SERVERS = "localhost:9092"

# Define city weather parameters
WEATHER_RANGES = {
    "Winnipeg": {"temp": (-30, 30), "wind": (0, 50), "humidity": (20, 80)},
    "Vancouver": {"temp": (-10, 25), "wind": (0, 30), "humidity": (30, 99)},
}

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def generate_weather_data():
    """Generates random weather data for Winnipeg and Vancouver."""
    city = random.choice(list(WEATHER_RANGES.keys()))
    params = WEATHER_RANGES[city]
    
    weather_data = {
        "city": city,
        "temperature": random.randint(*params["temp"]),
        "wind_speed": random.randint(*params["wind"]),
        "humidity": random.randint(*params["humidity"]),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),  # Fix timestamp format
    }

    return weather_data

def send_weather_data():
    """Sends generated weather data to Kafka."""
    while True:
        weather_data = generate_weather_data()
        producer.send(TOPIC_NAME, value=weather_data)
        log.info(f"📤 Sent data: {json.dumps(weather_data)}")
        time.sleep(5)

if __name__ == "__main__":
    log.info(f"Starting Kafka Producer for topic '{TOPIC_NAME}'...")
    send_weather_data()
