import os
from dotenv import find_dotenv,load_dotenv
import requests
load_dotenv()

dotenv_path = find_dotenv()

cert_path = os.getenv("CERT_PATH", True) # True forces full verification
print(cert_path)

api_key = os.getenv("API_KEY")


TRAIN_URL = "https://opendata.transport.nsw.gov.au/dataset/historical-gtfs-and-gtfs-realtime"

headers = {
    "Authorization":f"apikey {api_key}"
}
request_details = dict(
    headers = headers,
    stream=True
)

request_details['verify'] = cert_path

response = requests.get("https://api.transport.nsw.gov.au/v1/gtfs/schedule/sydneytrains",**request_details)
print(response)