import socket
import json
from db.db_handler import load_laps_from_mongo

def start_server(driver_code="LEC", host="0.0.0.0", port=5000):
    server = socket.socket()
    server.bind((host, port))
    server.listen(1)
    print(f"Listening for peers on {host}:{port}...")

    conn, addr = server.accept()
    print(f"Connected to peer: {addr}")

    laps_df = load_laps_from_mongo(driver_code)
    data = laps_df.to_dict(orient="records")
    conn.sendall(json.dumps(data).encode())

    conn.close()
    print("Data sent, connection closed.")

if __name__ == "__main__":
    start_server()
