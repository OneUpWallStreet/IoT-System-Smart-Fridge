from encryption_utils import *
from client_endpoint_test import *
import time
import board
import adafruit_dht
import subprocess
import cv2


# Initialize the DHT22 sensor
dhtDevice = adafruit_dht.DHT22(board.D4)

jacks_device = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"

# Maximum number of retries
MAX_RETRIES = 10

# Delay between retries in seconds
RETRY_DELAY = .5

def read_dht22(dht_device):
    for attempt in range(MAX_RETRIES):
        try:
            # Attempt to read the temperature and humidity from the sensor
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
            if temperature_c is not None and humidity is not None:
                return temperature_c, humidity
            else:
                # Data was None, which sometimes happens, so retry
                print(f"Attempt {attempt + 1} of {MAX_RETRIES}: Got None from the sensor, retrying...")
                time.sleep(RETRY_DELAY)
        except RuntimeError as e:
            # Log the error and wait before retrying
            print(f"Attempt {attempt + 1} of {MAX_RETRIES}: {e}, retrying...")
            time.sleep(RETRY_DELAY)

    # If we reach this point, all retries have failed
    print("Failed to read from DHT22 sensor after maximum retries.")
    return None, None  # Indicate failure


# Main loop
try:
    while True:

        # Read fresh sensor data
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temperature_f = (temperature_c * 9 / 5) + 32

        temperature_c, humidity = read_dht22(dhtDevice)
        if temperature_c is not None and humidity is not None:
            temperature_f = (temperature_c * 9 / 5) + 32
            print(f"Temperature: {temperature_f}°F, Humidity: {humidity}%")
        temperature_f = (temperature_c * 9 / 5) + 32
        # Upload sensor data
        response = humid_temp_upload(jacks_device, str(temperature_f), str(humidity), b'YourCameraAPIKey')
        print("Sensor data uploaded successfully.")

        # Wait for 15 min before reading sensor data again (Configurable to user preference)
        time.sleep(900)

except KeyboardInterrupt:
    print("Process terminated by user.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
