"Tests for data.stop"

import pandas as pd
import pytz

from data.stop import Stop
from data.trip import Trip

class TestTrip:

    def test_remove_irrelevant_records(self):
        "Test that records with departure_time = 0 or arrival time = 0 are removed, and duplicates are removed"

        df_in = pd.DataFrame({
             'trip_id': [1, 2, 3, 4, 2]
            ,'departure_time': [0, 100, 200, 0, 100]
            ,'arrival_time': [200, 100, 0, 0, 100]
            })
        
        df_out = pd.DataFrame({
             'trip_id': [2]
            ,'departure_time': [100]
            ,'arrival_time': [100]
            })
        
        stop = Stop()
        trip = Trip(stop)
        trip.df = df_in.copy()
        trip.remove_irrelevant_records()

        assert(trip.df.equals(df_out))

    def test_format_dates(self):
        "Test that dates are correctly converted from POSIX format to Sydney time"

        df_in = pd.DataFrame({
             'trip_id': [1, 2, 3]
            ,'time1': [1654070960, 1654068888, 1654068083]
            ,'time2': [1654068888, 1654068083, 1654070960]
            ,'time3': [200, 100, 0]
            })
        
        date_cols_to_format = ('time1', 'time2')
        
        df_out = pd.DataFrame({
             'trip_id': [1, 2, 3]
            ,'time1': ['2022-06-01 18:09:20+10:00', '2022-06-01 17:34:48+10:00', '2022-06-01 17:21:23+10:00']
            ,'time2': ['2022-06-01 17:34:48+10:00', '2022-06-01 17:21:23+10:00', '2022-06-01 18:09:20+10:00']
            ,'time3': [200, 100, 0]
            })
        df_out['time1'] = pd.to_datetime(df_out['time1']).dt.tz_convert(pytz.timezone('Australia/Sydney'))
        df_out['time2'] = pd.to_datetime(df_out['time2']).dt.tz_convert(pytz.timezone('Australia/Sydney'))
        
        stop = Stop()
        trip = Trip(stop)
        trip.df = df_in.copy()
        trip._date_cols_to_format = date_cols_to_format
        trip.format_dates()

        assert(trip.df.equals(df_out))

    def test_apply_mappings(self):
        "Test that mappings are applied correctly"

        df_in = pd.DataFrame({
             'trip_id': [2, 4, 1]
            ,'stop_id': [202, 404, 101]
            })
        
        df_stop = pd.DataFrame({
             'stop_id': [101, 202, 303, 404]
            ,'stop_station_name': ['A1', 'B2', 'C3', 'D4']
            ,'stop_platform_name': ['Platform 1', 'Platform 2', 'Platform 3', 'Platform 4']
            })

        df_out = pd.DataFrame({
             'trip_id': [2, 4, 1]
            ,'stop_id': [202, 404, 101]
            ,'stop_station_name': ['B2', 'D4', 'A1']
            ,'stop_platform_name': ['Platform 2', 'Platform 4', 'Platform 1']
            })
        
        stop = Stop()
        stop.df = df_stop.copy()

        trip = Trip(stop)
        trip.df = df_in.copy()
        trip.stop = stop
        trip.apply_mappings()

        assert(trip.df.equals(df_out))
        assert(len(trip.df) == len(df_in))
        assert(len(trip.df) == len(df_out))

    def test_filter_relevant_cols(self):
        "Test filter for relevant columns"

        df_in = pd.DataFrame({
             'trip_id': [2, 4, 1]
            ,'stop_id': [202, 404, 101]
            ,'stop_station_name': ['B2', 'D4', 'A1']
            ,'stop_platform_name': ['Platform 2', 'Platform 4', 'Platform 1']
            })
        
        data_cols_relevant = ['trip_id', 'stop_station_name', 'stop_platform_name']

        df_out = pd.DataFrame({
             'trip_id': [2, 4, 1]
            ,'stop_station_name': ['B2', 'D4', 'A1']
            ,'stop_platform_name': ['Platform 2', 'Platform 4', 'Platform 1']
            })
        
        stop = Stop()
        trip = Trip(stop)
        trip.df = df_in.copy()
        trip._data_cols_relevant = data_cols_relevant.copy()
        trip.filter_relevant_cols()

        assert(trip.df.equals(df_out))    


    def test_sort_trips(self):
        "Test filter for relevant columns"

        df_in = pd.DataFrame({
             'trip_id': [2, 4, 1]
            ,'current_stop_sequence': [202, 404, 101]
            })
        
        sort_cols = ['trip_id', 'current_stop_sequence']

        df_out = pd.DataFrame({
             'trip_id': [1, 2, 4]
            ,'current_stop_sequence': [101, 202, 404]
            })
        
        stop = Stop()
        trip = Trip(stop)
        trip.df = df_in.copy()
        trip._sort_cols = sort_cols.copy()
        trip.sort_trips()

        assert(trip.df.equals(df_out))    

    def test_process_data(self):
        "Test that all data processing is performed"

        df_in = pd.DataFrame({
             'trip_id': [1, 2, 3, 4, 2, 2]
            ,'stop_id': [101, 202, 303, 404, 202, 202]
            ,'current_stop_sequence': [101, 505, 303, 404, 202, 202]
            ,'departure_time': [0, 1654070960, 200, 0, 1654070960, 1654070960]
            ,'arrival_time': [200, 1654068888, 0, 0, 1654068888, 1654068888]
            })
        
        date_cols_to_format = ['departure_time', 'arrival_time']

        df_stop = pd.DataFrame({
             'stop_id': [101, 202, 303, 404]
            ,'stop_station_name': ['A1', 'B2', 'C3', 'D4']
            ,'stop_platform_name': ['Platform 1', 'Platform 2', 'Platform 3', 'Platform 4']
            })
        
        data_cols_relevant = ['trip_id', 'current_stop_sequence', 'departure_time', 'arrival_time', 'stop_station_name', 'stop_platform_name']

        sort_cols = ['trip_id', 'current_stop_sequence']

        df_out = pd.DataFrame({
             'trip_id': [2, 2]
            ,'current_stop_sequence': [202, 505]
            ,'departure_time': ['2022-06-01 18:09:20+10:00', '2022-06-01 18:09:20+10:00']
            ,'arrival_time': ['2022-06-01 17:34:48+10:00', '2022-06-01 17:34:48+10:00']
            ,'stop_station_name': ['B2', 'B2']
            ,'stop_platform_name': ['Platform 2', 'Platform 2']
            })
        df_out['departure_time'] = pd.to_datetime(df_out['departure_time']).dt.tz_convert(pytz.timezone('Australia/Sydney'))
        df_out['arrival_time'] = pd.to_datetime(df_out['arrival_time']).dt.tz_convert(pytz.timezone('Australia/Sydney'))


        stop = Stop()
        stop.df = df_stop.copy()
       
        trip = Trip(stop)
        trip.df = df_in.copy()
        trip._date_cols_to_format = date_cols_to_format.copy()
        trip._data_cols_relevant = data_cols_relevant.copy()
        trip._sort_cols = sort_cols.copy()

        trip.process_data()

        assert(trip.df.equals(df_out))

