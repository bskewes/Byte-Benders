"Fetch stops data"

import pandas as pd

class Stop():

    def __init__(self
                ,api_info
                ,data_cols):

        self.api_info = api_info
        self.data_cols = data_cols
        self.database = None
        self.df = None

        pass

    def download_data(self):

        pass

    def store_data(self):

        pass

    def process_data(self):
        # intended to run format_dates(), remove_duplicates()

        self.split_stop_station_and_platform_names()

        pass

    def split_stop_station_and_platform_names(self):

        self.df[['stop_station_name','stop_platform_name']] = self.df['stop_name'].str.split(', ', n=1, expand = True)
        self.df['stop_station_name'] = self.df['stop_station_name'].str.replace('Station', '').str.strip()

        pass
