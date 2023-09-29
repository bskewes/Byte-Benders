import os
from dotenv import find_dotenv,load_dotenv
import requests
load_dotenv()

dotenv_path = find_dotenv()

cert_path = os.getenv("CERT_PATH", True) # True forces full verification
print(cert_path)

api_key = os.getenv("API_KEY")

BASE = "https://api.transport.nsw.gov.au/"
TRAIN_URL = f"{BASE}v1/gtfs/schedule/sydneytrains"
TRAIN_REAL = f"{BASE}v2/gtfs/vehiclepos"

headers = {
    "Authorization":f"apikey {api_key}"
}
request_details = dict(
    headers = headers,
    stream=True
)

request_details['verify'] = cert_path

response = requests.get(TRAIN_URL,**request_details)
print(response)

