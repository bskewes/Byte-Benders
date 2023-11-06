# Need these to do the actual downloading
import os
from dotenv import load_dotenv
import requests
from google.transit import gtfs_realtime_pb2 # Parse feed
from protobuf_to_dict import protobuf_to_dict # Read from feed

import copy #so that I can use deepcopy

# Need these to run the analysis
from typing import List
import pandas as pd





load_dotenv()

cert_path = os.getenv("CERT_PATH", True) # True forces full verification

api_key = os.getenv("API_KEY")

BASE = "https://api.transport.nsw.gov.au/"
METRO_STATIC = f"{BASE}v1/gtfs/schedule/metro"
METRO_REALTIME_HISTORICAL = f"{BASE}v1/gtfs/historical"
METRO_REALTIME_CURRENT = f"{BASE}v1/gtfs/realtime/metro"
METRO_POSITION_URI = f"{BASE}v1/gtfs/vehiclepos/metro" # This part is added
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



# Static data

def download_static():
    response_static = requests.get(METRO_STATIC,**request_details)
    # curl -X 'GET' \
    #   'https://api.transport.nsw.gov.au/v1/gtfs/schedule/metro' \
    #   -H 'accept: application/octet-stream'
    print(response_static) # Response [200]

    with open(zip_path, "wb") as f:
        f.write(response_static.content)



# Historical realtime data - though would need to be able to capture the fromDate and toDate from an input ideally

def download_realtime_historical():
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



# Current realtime data
def download_realtime_current():
    response_realtime_current = requests.get(METRO_REALTIME_CURRENT,**request_details)
    # curl -X 'GET' \
    #   'https://api.transport.nsw.gov.au/v1/gtfs/realtime/metro' \
    #   -H 'accept: application/x-google-protobuf'
    print(response_realtime_current)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response_realtime_current.content)
    realtime_current = protobuf_to_dict(feed)
    return realtime_current
# Need to write a function for flattening this for use







# Current position data
def download_positions():
    response_positions = requests.get(METRO_POSITION_URI,**request_details)
    # curl -X 'GET' \
    #   'https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/metro' \
    #   -H 'accept: application/x-google-protobuf'
    print(response_positions) # Response [200]
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response_positions.content)
    positions = protobuf_to_dict(feed)
    return positions
# Is there no metro position data?? I think that's the case - then ignore position data
# Or is it because there's no metros at the current time?



def download_positions_bus():
    BUS_POSITION_URI =f"{BASE}v1/gtfs/vehiclepos/buses"
    response_positions = requests.get(BUS_POSITION_URI,**request_details)
    print(response_positions) # Response [200]
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response_positions.content)
    positions = protobuf_to_dict(feed)
    return positions

def download_positions_ferry():
    POSITION_URI =f"{BASE}v1/gtfs/vehiclepos/ferries/sydneyferries"
    response_positions = requests.get(POSITION_URI,**request_details)
    print(response_positions) # Response [200]
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response_positions.content)
    positions = protobuf_to_dict(feed)
    return positions

def download_positions_trains():
    POSITION_URI =f"{BASE}v2/gtfs/vehiclepos/sydneytrains"
    response_positions = requests.get(POSITION_URI,**request_details)
    print(response_positions) # Response [200]
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response_positions.content)
    positions = protobuf_to_dict(feed)
    return positions



# Schedule
def download_schedule():
    response_schedule = requests.get(METRO_SCHEDULE, **request_details) # Response [200]
    # curl -X 'GET' \
    #   'https://api.transport.nsw.gov.au/v1/gtfs/schedule/metro' \
    #   -H 'accept: application/octet-stream'
    print(response_schedule)

    with open(zip_path, "wb") as f:
        f.write(response_schedule.content)



# Alerts
def download_alerts():
    response_alerts = requests.get(METRO_ALERTS, **request_details) # Response [200]
    # curl -X 'GET' \
    #   'https://api.transport.nsw.gov.au/v2/gtfs/alerts/metro' \
    #   -H 'accept: application/x-google-protobuf'
    print(response_alerts)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response_alerts.content)
    alerts = protobuf_to_dict(feed)
    return alerts







### ANALYSIS PART ###

# Borrow their code for flattening
def flatten_entity(position:dict) -> dict:
    """
    live data arrives in the following format and needs to be flattened:
    {
        'id': '33553_26249868_2436_600_1',
        'vehicle': {
            'trip': {
                'trip_id': '1954191',
                'start_time': '19:40:00',
                'start_date': '20230911',
                'schedule_relationship': 0,
                'route_id': '2436_600'
            },
            'position': {
                'latitude': -33.71885299682617,
                'longitude': 151.10745239257812,
                'bearing': 44.0,
                'speed': 15.300000190734863
            },
            'timestamp': 1694428312,
            'congestion_level': 1,
            'vehicle': {
                'id': '33553_26249868_2436_600_1'
            },
            'occupancy_status': 1
        }
    }

    Args:
        position (dict): _description_

    Returns:
        dict: _description_
    """
    row = {}
    row["id"] = position["id"]

    trip = position["vehicle"]["trip"]
    row["trip_id"] = trip.get("trip_id","")
    row["route_id"] = trip.get("route_id","")
    row["schedule_relationship"] = trip.get("schedule_relationship","")

    if "position" in position['vehicle']:
        row["lat"] = position["vehicle"]["position"].get("latitude","")
        row["lon"] = position["vehicle"]["position"].get("longitude","")
        row["bearing"] = position["vehicle"]["position"].get("bearing","")
        row["speed"] = position["vehicle"]["position"].get("speed","")
    else:
        # Example for debugging, too few Nones
        row['lat'], row['lon'], row['bearing'], row['speed'] = None, None, None, None
    
    row["timestamp"] = position["vehicle"].get("timestamp","")
    row["congestion_level"] = position["vehicle"].get("congestion_level","")
    row["stop_id"] = position["vehicle"].get("stop_id","")
    row["vehicle_id"] = position["vehicle"]["vehicle"].get("id","")
    row["label"] = position["vehicle"]["vehicle"].get("label","")

    return row



def flatten_realtime_current():
    """
    Trip update
    Trip - trip_id, start_time, start_date, schedule_relationship, route_id (can ignore)
    stop_time_update
        stop_sequence
            departure
                delay
                time
            stop_id
            schedule_relationship (inore)
        arrival
            delay
            time
    Just extract arrival and departure delay and time for now, and stop sequence
    """

    row = {}
    row["id"] = realtime_current["id"]

    trip = realtime["trip_update"]["trip"]
    row["trip_id"] = trip.get("trip_id","")
    row["start_time"] = trip.get("start_time","")
    row["start_date"] = trip.get("start_date","")
    row["schedule_relationship"] = trip.get("schedule_relationship","")
    row["route_id"] = trip.get("route_id","")

    return row



        """
    {'header': {
'gtfs_realtime_version': '1.0', 
'incrementality': 0, 
'timestamp': 1699281059
}, 
'entity': [{
'id': '20231107_013059_1', 
'trip_update': {
'trip': {
'trip_id': '124-15.071123.30.0007', 
'start_time': '00:07:00', 
'start_date': '20231107', 
'schedule_relationship': 0, 
'route_id': 'SMNW_M'
}, 
'stop_time_update': [{
'stop_sequence': 1, 
'departure': {
'delay': 19, 
'time': 1699276039
}, 
'stop_id': '2067143', 
'schedule_relationship': 0
}, {
'stop_sequence': 2, 
'arrival': {
'delay': -30, 
'time': 1699276289
}, 
'departure': {
'delay': 24, 
'time': 1699276344
}, 
'stop_id': '2113362', 
'schedule_relationship': 0
}, {
'stop_sequence': 3, 
'arrival': {
'delay': -35, 
'time': 1699276404
}, 
'departure': {
'delay': 17, 
'time': 1699276457
}, 
'stop_id': '2113342', 
'schedule_relationship': 0
}, {
'stop_sequence': 4, 
'arrival': {
'delay': -48, 
'time': 1699276511
}, 
'departure': {
'delay': 7, 
'time': 1699276567
}, 
'stop_id': '2113352',
‘schedule_relationship': 0
}, {'stop_sequence': 5,
‘arrival': {
'delay': -72,
‘time': 1699276727
},
‘departure': {
'delay': -14,
‘time': 1699276785
},
‘stop_id': '2121226',
‘schedule_relationship': 0
}, {
'stop_sequence': 6,
‘arrival':
{
'delay': -35,
‘time': 1699277064
},
‘departure':
{
'delay': 19,
‘time': 1699277119
},
‘stop_id': '2126160',
‘schedule_relationship': 0
}, {
'stop_sequence': 7,
‘arrival':
{
'delay': -58,
‘time': 1699277221
},
‘departure':
{
'delay': -1,
‘time': 1699277278
},
‘stop_id': '2154263',
‘schedule_relationship': 0
}, {
'stop_sequence': 8,
‘arrival':
{
'delay': -29,
‘time': 1699277370
},
‘departure':
{
'delay': 26,
‘time': 1699277426
},
‘stop_id': '2154265',
‘schedule_relationship': 0
}, {
'stop_sequence': 9,
‘arrival':
{
'delay': -55,
‘time': 1699277524
},
‘departure':
{
'delay': 0,
‘time': 1699277580
},
‘stop_id': '2153405',
‘schedule_relationship': 0
}, {
'stop_sequence': 10,
‘arrival':
{
'delay': -20,
‘time': 1699277679
},
‘departure':
{
'delay': 32,
‘time': 1699277732
},
‘stop_id': '2153403',
‘schedule_relationship': 0
}, {
'stop_sequence': 11,
‘arrival':
{
'delay': -56,
‘time': 1699277823
},
‘departure':
{
'delay': 4,
‘time': 1699277884
},
‘stop_id': '2155266',
‘schedule_relationship': 0
}, {
'stop_sequence': 12,
‘arrival':
{
'delay': -64,
‘time': 1699277995
},
‘departure':
{
'delay': -8,
‘time': 1699278051
},
‘stop_id': '2155268',
‘schedule_relationship': 0
}, {
'stop_sequence': 13,
‘arrival':
{
'delay': -30,
‘time': 1699278149
},
‘stop_id': '2155270',
‘schedule_relationship': 0
}],
‘vehicle':
{
'id': '34',
‘label': '12:07am Chatswood - Tallawong',
‘license_plate': ''
}
}
}, {
'id': '20231107_013059_2',
‘trip_update':
{
'trip':
{
'trip_id': '133-02.301023.15.2355',
‘start_time': '23:55:00',
‘start_date': '20231106',
‘schedule_relationship': 0,
‘route_id': 'SMNW_M'
},
‘stop_time_update': [{
'stop_sequence': 1,
‘departure':
{
'delay': 18,
‘time': 1699275318
},
‘stop_id': '2155269',
‘schedule_relationship': 0
}, {
'stop_sequence': 2,
‘arrival':
{
'delay': -13,
‘time': 1699275406
},
‘departure':
{
'delay': 42,
‘time': 1699275462
},
‘stop_id': '2155267',
‘schedule_relationship': 0
}, {
'stop_sequence': 3,
‘arrival':
{
'delay': -26,
‘time': 1699275573
},
‘departure':
{
'delay': 29,
‘time': 1699275629
},
‘stop_id': '2155265',
‘schedule_relationship': 0
}, {
'stop_sequence': 4,
‘arrival':
{
'delay': 0,
‘time': 1699275719
},
‘departure':
{
'delay': 54,
‘time': 1699275774
},
‘stop_id': '2153402',
‘schedule_relationship': 0
}, {
'stop_sequence': 5,
‘arrival':
{
'delay': -27,
‘time': 1699275872
},
‘departure':
{
'delay': 27,
‘time': 1699275927
},
‘stop_id': '2153404',
‘schedule_relationship': 0
}, {
'stop_sequence': 6,
‘arrival':
{
'delay': 
11,
‘time': 1699276031
},
‘departure':
{
'delay': 66,
‘time': 1699276086
},
‘stop_id': '2154264',
‘schedule_relationship': 0
}, {
'stop_sequence': 7,
‘arrival':
{
'delay': -22,
‘time': 1699276177
},
‘departure':
{
'delay': 31,
‘time': 1699276231
},
‘stop_id': '2154262',
‘schedule_relationship': 0
}, {
'stop_sequence': 8,
‘arrival':
{
'delay': 17,
‘time': 1699276337
},
‘departure':
{
'delay': 75,
‘time': 1699276395
},
‘stop_id': '2126159',
‘schedule_relationship': 0
}, {
'stop_sequence': 9,
‘arrival':
{
'delay': 0,
‘time': 1699276679
},
‘departure':
{
'delay': 58,
‘time': 1699276738
},
‘stop_id': '2121225',
‘schedule_relationship': 0
}, {
'stop_sequence': 10,
‘arrival':
{
'delay': -24,
‘time': 1699276895
},
‘departure':
{
'delay': 30,
‘time': 1699276950
},
‘stop_id': '2113351',
‘schedule_relationship': 0
}, {
'stop_sequence': 11,
‘arrival':
{
'delay': -29,
‘time': 1699277010
},
‘departure':
{
'delay': 26,
‘time': 1699277066
},
‘stop_id': '2113341',
‘schedule_relationship': 0
}, {
'stop_sequence': 12,
‘arrival':
{
'delay': -35,
‘time': 1699277124
},
‘departure':
{
'delay': 20,
‘time': 1699277180
},
‘stop_id': '2113361',
‘schedule_relationship': 0
}, {
'stop_sequence': 13,
‘arrival':
{
'delay': -13,
‘time': 1699277446
},
‘stop_id': '2067142',
‘schedule_relationship': 0
}],
‘vehicle':
{
'id': '15',
‘label': '11:55pm Tallawong - Chatswood',
‘license_plate': ''
}
}
}]
}

    """


# Their code
def get_positions_dataframe(positions:List[dict]) -> pd.DataFrame:
    # Example for debugging: Forget to search for ['entity']
    df = pd.DataFrame([flatten_entity(e) for e in positions['entity']])
    df['request_timestamp'] = positions['header']['timestamp']
    return df

# Update for our use
def realtime_current_dataframe(realtime_current:List[dict]) -> pd.DataFrame:
    # Example for debugging: Forget to search for ['entity']
    df = pd.DataFrame([flatten_realtime_current(e) for e in realtime_current['entity']])
    df['request_timestamp'] = realtime_current['header']['timestamp']
    return df

def fetch_positions():
    positions = download_positions_bus()
    df = get_positions_dataframe(positions)
    return df


def fetch_realtime_current():
    realtime_current = download_realtime_current()
    df = realtime_current_dataframe(realtime_current)
    return df
