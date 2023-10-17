"Fetch realtime data: trip"

from data.stop import Stop
from data.trip import Trip

def update_realtime_data():

    stop = Stop()
    # TODO replace temporary method with read_in_data per below
    # stop.read_in_data()
    
    # temporary method until SQL Lite implemented
    stop.download_data()
    stop.process_data()

    trip = Trip(stop)
    trip.download_data()
    trip.process_data()
    trip.store_data()

    print(trip.df)



if __name__ == "__main__":
    update_realtime_data()
