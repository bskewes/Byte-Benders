## run tests by typing the following in cmd: python -m pytest
## pytest.ini specifies where all the tests are stored

import pytest

import pandas as pd

from data.stop import Stop
from data.route import Route
from data.trip import Trip
from analysis.relevant_trips import RelevantTrips

class TestStop:

    def test_split_stop_station_and_platform_names(self):
        
        df_in = pd.DataFrame({
             'trip_id': [1, 2, 3]
            ,'stop_name': ['X Station, Platform 1', 'Y Station, Platform 2', 'Z Station, Platform 3']
            })
        
        df_out = pd.DataFrame({
             'trip_id': [1, 2, 3]
            ,'stop_name': ['X Station, Platform 1', 'Y Station, Platform 2', 'Z Station, Platform 3']
            ,'stop_station_name': ['X', 'Y', 'Z']
            ,'stop_platform_name': ['Platform 1', 'Platform 2', 'Platform 3']
            })
        
        stop = Stop(api_info = '', data_cols = [''])
        stop.df = df_in.copy()
        stop.split_stop_station_and_platform_names()

        assert(stop.df.equals(df_out))

    def test_process_data(self):

        df_in = pd.DataFrame({
             'trip_id': [1, 2, 3]
            ,'stop_name': ['X Station, Platform 1', 'Y Station, Platform 2', 'Z Station, Platform 3']
            })
        
        df_out = pd.DataFrame({
             'trip_id': [1, 2, 3]
            ,'stop_name': ['X Station, Platform 1', 'Y Station, Platform 2', 'Z Station, Platform 3']
            ,'stop_station_name': ['X', 'Y', 'Z']
            ,'stop_platform_name': ['Platform 1', 'Platform 2', 'Platform 3']
            })
        
        stop = Stop(api_info = '', data_cols = [''])
        stop.df = df_in.copy()
        stop.process_data()

        assert(stop.df.equals(df_out))