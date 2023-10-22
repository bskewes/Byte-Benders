import os
from dotenv import load_dotenv
import requests
from google.transit import gtfs_realtime_pb2


load_dotenv()

cert_path = os.getenv("CERT_PATH", True) # True forces full verification

api_key = os.getenv("API_KEY")

BASE = "https://api.transport.nsw.gov.au/"
# TRAIN_URL = f"{BASE}v1/gtfs/schedule/sydneytrains" # TODO - leave for testing, delete when done
# TRAIN_REAL = f"{BASE}v2/gtfs/vehiclepos" # TODO - leave for testing, delete when done

METRO_STATIC = f"{BASE}v1/gtfs/schedule/metro"
METRO_REALTIME = f"{BASE}v1/gtfs/v1/gtfs/historical"

headers = {
    "Authorization":f"apikey {api_key}"
}
request_details = dict(
    headers = headers,
    stream=True
)

request_details['verify'] = cert_path

# response = requests.get(TRAIN_URL,**request_details)
# print(response)
# response = requests.get(TRAIN_REAL,**request_details)
# print(response)

response_static = requests.get(METRO_STATIC,**request_details)
print(response_static)
response_realtime = requests.get(METRO_REALTIME,**request_details) # TODO - fix - still getting response 500 for now
print(response_realtime)
