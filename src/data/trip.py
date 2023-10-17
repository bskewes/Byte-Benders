"Fetch real-time / historical trip data"

import pandas as pd
import pytz

from data.stop import Stop

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Trip():

    def __init__(self
                ,stop: Stop):

        # TODO need to fill in the fixed info for these parameters (except for df)

        self._api_info = None
        self._data_cols = None

        self._date_cols_to_format = ['departure_time', 'arrival_time']
        self._data_cols_relevant = ['trip_id','vehicle_label'
                                    ,'current_stop_sequence','stop_id', 'stop_station_name', 'stop_platform_name'
                                    ,'start_date','start_time','departure_delay','departure_time','arrival_delay','arrival_time']
        self._sort_cols = ['trip_id','current_stop_sequence']
        self._database = None
        self._table_name = None

        self.stop = stop

        self.df = None

        pass

    def download_data(self):
        # TODO uses self.api_info and self.data_cols

        # below is temporary method until SQL Lite is implemented
        sample_realtime_data_path = Path(os.getenv("DATA_PATH")) / 'Historical GTFS and GTFS Realtime - Metro'

        self.df = pd.read_csv(sample_realtime_data_path / 'TripUpdate_20220601.csv')

    def process_data(self):

        self.remove_irrelevant_records()
        self.format_dates()
        self.apply_mappings()
        self.filter_relevant_cols()
        self.sort_trips()

    def remove_irrelevant_records(self):

        self.df = self.df[(self.df['departure_time'] != 0)
                          & (self.df['arrival_time'] != 0)]     \
                          .drop_duplicates()    \
                          .reset_index(drop = True)

    def format_dates(self):

        for col_name in self._date_cols_to_format:
            self.df[col_name] = pd.to_datetime(self.df[col_name], unit = 's', utc = True).dt.tz_convert(pytz.timezone('Australia/Sydney'))

    def apply_mappings(self):

        self.df = self.df.merge(self.stop.df, how = 'left', on = ['stop_id'], copy = True)

    def filter_relevant_cols(self):

        self.df = self.df[self._data_cols_relevant]

    def sort_trips(self):

        self.df = self.df.sort_values(self._sort_cols)  \
                        .reset_index(drop = True)

    def store_data(self):
        # TODO uses self.database and self.table_name

        pass

    def read_in_data(self):
        # TODO uses self.database and self.table_name

        pass
