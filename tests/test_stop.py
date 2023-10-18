"Tests for data.stop"

import pandas as pd

from data.stop import Stop

class TestStop:

    def test_split_stop_station_and_platform_names(self):
        "Test that the stop_name field is split appropriately into stop_station_name and stop_platform_name"
        
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
        
        stop = Stop()
        stop.df = df_in.copy()
        stop.split_stop_station_and_platform_names()

        assert(stop.df.equals(df_out))

    def test_process_data(self):
        "Test that all data processing is performed"

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
        
        stop = Stop()
        stop.df = df_in.copy()
        stop.process_data()

        assert(stop.df.equals(df_out))


