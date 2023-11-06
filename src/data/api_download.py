import os
from dotenv import load_dotenv
import requests
from google.transit import gtfs_realtime_pb2

import copy #so that I can use deepcopy


load_dotenv()

cert_path = os.getenv("CERT_PATH", True) # True forces full verification

api_key = os.getenv("API_KEY")

BASE = "https://api.transport.nsw.gov.au/"
METRO_STATIC = f"{BASE}v1/gtfs/schedule/metro"
METRO_REALTIME_HISTORICAL = f"{BASE}v1/gtfs/v1/gtfs/historical"
METRO_REALTIME_CURRENT = f"{BASE}v1/gtfs/realtime/metro"
METRO_POSITION_URL = f"{BASE}v1/gtfs/vehiclepos/metro" # This part is added
METRO_SCHEDULE = "https://api.transport.nsw.gov.au/v1/gtfs/schedule/metro"
METRO_ALERTS = "https://api.transport.nsw.gov.au/v2/gtfs/alerts/metro"



headers = {
    "Authorization":f"apikey {api_key}"
}
request_details = dict(
    headers = headers,
    stream=True
)
request_details['verify'] = cert_path

data = {
    "fromDate": "2020-08-11",
    "schemaType": "TripUpdate",
    "serviceName": "Metro",
    "toDate": "2020-08-12",
    "transportMode": "MET"
}

request_details_post = copy.deepcopy(request_details)
request_details_post['json'] = data



response_static = requests.get(METRO_STATIC,**request_details)
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/schedule/metro' \
#   -H 'accept: application/octet-stream'
print(response_static) # Response [200]

with open(zip_path, "wb") as f:
    f.write(response_static.content)


feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response_static.content)




response_realtime_historical = requests.post(METRO_REALTIME_HISTORICAL,**request_details_post)
# curl -X 'POST' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/historical' \
#   -H 'accept: application/json' \
#   -H 'Authorization: apikey eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ3VmxfUnlrek5uZy0wNE1rYm5ETmFlbkZ6YkxzX1ZQbkZYQmJVR2hFSnpjIiwiaWF0IjoxNjk1ODkzMDM0fQ.CuBpBqHbDI5GGpTc2T3xcmFXsJrfLetbi5TQRkV8IvI' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "fromDate": "2020-08-11",
#   "schemaType": "TripUpdate",
#   "serviceName": "Metro",
#   "toDate": "2020-08-12",
#   "transportMode": "MET"
# }'
print(response_realtime_historical) # Response [200]

with open(zip_path, "wb") as f:
    f.write(response_realtime_historical.content)

response_realtime_current = requests.get(METRO_REALTIME_CURRENT,**request_details)
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/realtime/metro' \
#   -H 'accept: application/x-google-protobuf'
print(response_realtime_current)

response_position = requests.get(METRO_POSITION_URL,**request_details)
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/metro' \
#   -H 'accept: application/x-google-protobuf'
print(response_position) # Response [200]

response_schedule = requests.get(METRO_SCHEDULE, **request_details) # Response [200]
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/schedule/metro' \
#   -H 'accept: application/octet-stream'
print(response_schedule)

response_alerts = requests.get(METRO_ALERTS, **request_details) # Response [200]
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v2/gtfs/alerts/metro' \
#   -H 'accept: application/x-google-protobuf'
print(response_alerts)