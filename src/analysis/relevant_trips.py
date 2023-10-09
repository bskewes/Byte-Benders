"Validate relevant trips, produce analyses, outputs and visualisation"

from data.stop import Stop
from data.route import Route
from data.trip import Trip

class RelevantTrips():

    def __init__(self
                ,stops
                ,stop: Stop
                ,route: Route
                ,trip: Trip):

        self.stops = stops
        self.stop = stop
        self.route = route
        self.trip = trip

        pass

    def validate_user_inputs(self):
        # intended to run all validation steps below

        pass

    def validate_stop_exists(self):

        pass

    def validate_route_exists(self):

        pass

    def validate_trip_exists(self):

        pass

    def extract_relevant_trips(self):

        pass

    def calculate_historical_delays(self):

        pass

    def produce_output(self):

        pass

    def produce_visualisation(self):

        pass
