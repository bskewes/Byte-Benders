"Fetch stops data"

import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Stop():

    def __init__(self):
        # TODO need to fill in the fixed info for these parameters (except for df)

        self._api_info = None
        self._data_cols = None
        self._database = None
        self._table_name = None

        self.df = None

        pass

    def download_data(self):
        # TODO uses self.api_info and self.data_cols

        # below is temporary method until SQL Lite is implemented
        sample_static_data_path = Path(os.getenv("DATA_PATH")) / 'Timetables Complete GTFS'

        self.df = pd.read_csv(sample_static_data_path / 'stops.txt')

    def process_data(self):

        self.split_stop_station_and_platform_names()

    def split_stop_station_and_platform_names(self):

        self.df[['stop_station_name','stop_platform_name']] = self.df['stop_name'].str.split(', ', n=1, expand = True)
        self.df['stop_station_name'] = self.df['stop_station_name'].str.replace('Station', '').str.strip()

    def store_data(self):
        # TODO uses self.database and self.table_name

        pass

    def read_in_data(self):
        # TODO uses self.database and self.table_name

        pass
