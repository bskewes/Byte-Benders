### Copied from the api_download file ###

import os
from dotenv import load_dotenv
import requests
from google.transit import gtfs_realtime_pb2 # need for realtime
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import MessageToJson
from protobuf_to_dict import protobuf_to_dict


# https://opendata.transport.nsw.gov.au/dataset/historical-gtfs-and-gtfs-realtime
# https://opendata.transport.nsw.gov.au/dataset/timetables-complete-gtfs



load_dotenv(override=True)

cert_path = os.getenv("CERT_PATH", True) # True forces full verification

api_key = os.getenv("API_KEY")

BASE = "https://api.transport.nsw.gov.au/"

### KEPT FOR TESTING

METRO_STATIC = f"{BASE}v1/gtfs/schedule/metro"
METRO_REALTIME = f"{BASE}v1/gtfs/historical"

METRO_REAL = "https://api.transport.nsw.gov.au/v1/gtfs/historical"



headers = {
    "Authorization":f"apikey {api_key}"
}
request_details = dict(
    headers = headers,
    stream=True
)

params = {{
    "fromDate": "2020-08-11",
    "schemaType": "TripUpdate",
    "serviceName": "Metro",
    "toDate": "2020-08-12",
    "transportMode": "MET"
}}
request_details2 = dict(
    headers = headers,
    stream=True,   
)

# https://curlconverter.com/
# curl -X 'POST' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/historical' \
#   -H 'accept: application/json' \
#   -d '{
#   "fromDate": "2020-08-11",
#   "schemaType": "TripUpdate",
#   "serviceName": "Metro",
#   "toDate": "2020-08-12",
#   "transportMode": "MET"
# }'
params = '{\n  "fromDate": "2020-08-11",\n  "schemaType": "TripUpdate",\n  "serviceName": "Metro",\n  "toDate": "2020-08-12",\n  "transportMode": "MET"\n}'
params = (
    ("fromDate", "2020-08-11"),
    ("schemaType", "TripUpdate"),
    ("serviceName", "Metro"),
    ("toDate", "2020-08-11"),
    ("transportMode", "MET")
)


# {
#   "fromDate": "2020-10-11",
#   "schemaType": "TripUpdate",
#   "serviceName": "SydneyFerries",
#   "toDate": "2020-10-11",
#   "transportMode": "FER"
# }


params = (
    ("fromDate", "2020-08-11"),
    ("schemaType", "TripUpdate"),
    ("serviceName", "Metro"),
    ("toDate", "2020-08-11"),
    ("transportMode", "MET")
)



request_details['verify'] = cert_path

request_details2['verify'] = cert_path
request_details2['data'] = params

request_details3 = dict(
    headers = headers,
    stream=True,   
)
request_details3['verify'] = cert_path
request_details3['json'] = params




### KEPT FOR TESTING
TRAIN_URL = f"{BASE}v1/gtfs/schedule/sydneytrains" # TODO - leave for testing, delete when done
response_train_url = requests.get(TRAIN_URL,**request_details)
print(response_train_url) # Response [200]

TRAIN_REAL = f"{BASE}v2/gtfs/vehiclepos/sydneytrains" # TODO - leave for testing, delete when done
response_real = requests.get(TRAIN_REAL,**request_details)
print(response_real) # Response [200]

response_static = requests.get(METRO_STATIC,**request_details)
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/schedule/metro' \
#   -H 'accept: application/octet-stream'
print(response_static) # Response [200]




feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response_static.content)



response_realtime = requests.get(METRO_REALTIME,**request_details) # TODO - fix - still getting response 500 for now
print(response_realtime) # Response [500]

response_realtime = requests.get(METRO_REAL,**request_details2) # TODO - fix - still getting response 500 for now
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
# https://stackoverflow.com/questions/15900338/python-request-post-with-param-data
print(response_realtime) # Response [500]


response_historical = requests.post(METRO_REAL,**request_details2)
print(response_historical) # Response [404]

response_historical = requests.post(METRO_REAL,**request_details3)
print(response_historical) # Response [200]

    with open(zip_path, "wb") as f:
        f.write(response_historical.content)


response_historical = requests.post(METRO_REAL,**request_details)
print(response_historical)




LINK_TRIAL = f"{BASE}v1/gtfs/realtime/metro"
response_trial = requests.get(LINK_TRIAL,**request_details) # Testing different links
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/realtime/metro' \
#   -H 'accept: application/x-google-protobuf'
print(response_trial) # Response [200]
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response_trial.content)

response_trial = requests.post(LINK_TRIAL,**request_details) # Testing different links
print(response_trial) # Response [500]











BASE_URL = "https://api.transport.nsw.gov.au"


response_trial = requests.get(BUS_POSITION_URI,**request_details) # Testing different links
print(response_trial) # Response [200]


BUS_POSITION_URI = f"{BASE_URL}/v1/gtfs/vehiclepos/buses"
BUS_POSITION_URL = f"{BASE}v1/gtfs/vehiclepos/buses" # This part is added
BUS_SCHEDULE_URI = f"{BASE_URL}/v1/gtfs/schedule/buses"
response_trial = requests.get(BUS_SCHEDULE_URI,**request_details) # Testing different links
print(response_trial) # Response [200]

FERRY_POSITION = f"{BASE_URL}/v1/gtfs/historical"
response_trial = requests.get(FERRY_POSITION,**request_details) # Testing different links
print(response_trial) # Response [500]

METRO_POSITION_URL = f"{BASE}v1/gtfs/vehiclepos/metro" # This part is added
response_trial = requests.get(METRO_POSITION_URL,**request_details)
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/metro' \
#   -H 'accept: application/x-google-protobuf'
print(response_trial) # Response [200]

TRAFFIC = f"{BASE_URL}/traffic/historicaldata"
response_trial = requests.get(TRAFFIC,**request_details)
print(response_trial) # Response [500]


METRO_SCHEDULE = "https://api.transport.nsw.gov.au/v1/gtfs/schedule/metro"
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v1/gtfs/schedule/metro' \
#   -H 'accept: application/octet-stream'
response_trial = requests.get(METRO_SCHEDULE, **request_details) # Response [200]
print(response_trial)

METRO_ALERTS = "https://api.transport.nsw.gov.au/v2/gtfs/alerts/metro"
# curl -X 'GET' \
#   'https://api.transport.nsw.gov.au/v2/gtfs/alerts/metro' \
#   -H 'accept: application/x-google-protobuf'
response_trial = requests.get(METRO_ALERTS, **request_details) # Response [200]
print(response_trial)


# METRO historical realtime
response_trial = requests.get(url = "https://api.transport.nsw.gov.au/v1/gtfs/historical",
                              headers = headers,
                              stream = True,
                              verify = cert_path,
                              params = params)
print(response_trial)



response_bus = requests.get(BUS_POSITION_URL, **request_details)
print(response_bus)
feed=gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response_bus.content)
positions = protobuf_to_dict(feed)



### download_gtfs ####
### copied from their file ###

FILENAME_SCHEDULE = 'gtfs.zip'
app_name = os.getenv("APP_NAME")
api_key = os.getenv("API_KEY")

BASE_URL = "https://api.transport.nsw.gov.au"
BUS_POSITION_URI = f"{BASE_URL}/v1/gtfs/vehiclepos/buses"
BUS_SCHEDULE_URI = f"{BASE_URL}/v1/gtfs/schedule/buses"
FERRY_POSITION = f"{BASE_URL}/v1/gtfs/historical"


    headers = {
        "Authorization": f"apikey {api_key}"
    }
    request_details = {
        "timeout": 50,
        "headers": headers,
        "stream": True
    }
    # On our network, we need to add a certificate or the request will fail
    # Look at the readme for instructions on how to set this up
    if cert:=os.getenv("CERT", None):
        request_details['verify'] = cert

    response = requests.get(BUS_SCHEDULE_URI, **request_details)

    with open(zip_path, "wb") as f:
        f.write(response.content)


### uplad gtfs files ###
### Don't actualyl need the upload part... ###
### How does the SQL Lite part work - may need to watch the video ###



    with zipfile.ZipFile(zip_path) as z:
        for table in _gtfs_table_registry_:
            print(table.__tablename__)
            with z.open(f"{table._gtfs_file_}.txt") as f:
                table_data = get_df(table, f)
                replace_table(table, table_data)





### Reading through the api.ipynb from their thing ###

# Taking apart their realtime file

# realtime.get_latest_positions

response_bus = requests.get(BUS_POSITION_URI, **request_details)
feed=gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response_bus.content)
positions = protobuf_to_dict(feed)

# realtime.get_positions_dataframe

