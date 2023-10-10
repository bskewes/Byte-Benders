"Fetch real-time / historical trip data"

from data.stop import Stop
from data.route import Route

class Trip():

    def __init__(self
                ,api_info
                ,data_cols
                ,stop: Stop
                ,route: Route):

        self.api_info = api_info
        self.data_cols = data_cols
        self.stop = stop
        self.route = route

        pass

    def download_data(self):

        pass

    def store_data(self):

        pass

    def process_data(self):
        # intended to run format_dates(), remove_duplicates(), apply_mapping()

        pass

    def format_dates(self):

        pass

    def remove_duplicates(self):

        pass

    def apply_mappings(self):

        pass

