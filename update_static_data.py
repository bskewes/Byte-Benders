"Fetch static data: stop"

from data.stop import Stop

def update_static_data():

    stop = Stop()
    stop.download_data()
    stop.process_data()
    stop.store_data()

    print(stop.df)



if __name__ == "__main__":
    update_static_data()
