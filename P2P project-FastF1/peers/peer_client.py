import socket
import json
import pandas as pd
from db.db_handler import save_laps_to_mongo

def connect_to_peer(host="127.0.0.1", port=5000, driver_code="PEER"):
    client = socket.socket()
    client.connect((host, port))
    print("Connected to peer server.")

    data = b""
    while True:
        part = client.recv(4096)
        if not part:
            break
        data += part

    lap_list = json.loads(data.decode())
    df = pd.DataFrame(lap_list)
    save_laps_to_mongo(driver_code, df)
    print(f"Received and saved {len(df)} laps as {driver_code}.")

    client.close()

if __name__ == "__main__":
    connect_to_peer()
