from fetch.fetch_f1_data import fetch_race_data
from db.db_handler import save_laps_to_mongo, load_laps_from_mongo
from peers.peer_server import start_server
from peers.peer_client import connect_to_peer
from analysis.compare_stats import plot_lap_time_comparison
import pandas as pd

def main():
    while True:
        print("\nP2P FastF1: Select an option")
        print("1. Fetch and save race data")
        print("2. Share data with a peer (run server)")
        print("3. Receive data from peer (run client)")
        print("4. Compare your data with peer's data")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            year = int(input("Enter season year (e.g. 2023): "))
            gp = input("Enter Grand Prix name (e.g. Italian Grand Prix): ")
            driver = input("Save as driver code (e.g. LEC): ")

            laps_df = fetch_race_data(year, gp)
            laps_df = laps_df[laps_df['Driver'] == driver]  # Filter to only that driver
            save_laps_to_mongo(driver, laps_df)

        elif choice == "2":
            driver_code = input("Which driver’s data to share (e.g. LEC)? ")
            port = int(input("Enter port to run server on (default 5000): ") or 5000)
            start_server(driver_code=driver_code, port=port)

        elif choice == "3":
            ip = input("Enter peer IP (e.g. 127.0.0.1): ")
            port = int(input("Enter peer port (default 5000): ") or 5000)
            driver_code = input("Save peer data as (e.g. PEER): ")
            connect_to_peer(host=ip, port=port, driver_code=driver_code)

        elif choice == "4":
            d1 = input("Your driver code (e.g. LEC): ")
            d2 = input("Peer driver code (e.g. PEER): ")
            plot_lap_time_comparison(d1, d2)

        elif choice == "5":
            print("Exiting... Good race!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
