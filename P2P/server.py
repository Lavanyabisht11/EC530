import socket
import threading
import logging

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []  # List to keep track of connected clients
        self.lock = threading.Lock()  # To handle concurrent access to clients list

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Listen for up to 5 incoming connections
        logging.info(f"Server listening on {self.host}:{self.port}")

        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                logging.info(f"Accepted connection from {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.start()
                with self.lock:
                    self.clients.append((client_socket, addr))
            except KeyboardInterrupt:
                logging.info("Server shutting down...")
                break
            except Exception as e:
                logging.error(f"Error accepting connection: {e}")

        self.close()

    def handle_client(self, client_socket, addr):
        try:
            while True:
                try:
                    data = client_socket.recv(1024)  # Receive up to 1024 bytes
                    if not data:
                        logging.info(f"Client {addr} disconnected.")
                        break
                    message = data.decode('utf-8').strip()
                    logging.info(f"Received from {addr}: {message}")
                    self.broadcast(f"[{addr[0]}:{addr[1]}] {message}", client_socket)
                except ConnectionResetError:
                    logging.info(f"Connection reset by {addr}")
                    break
                except Exception as e:
                    logging.error(f"Error handling client {addr}: {e}")
                    break
        finally:
            self.remove_client(client_socket, addr)
            client_socket.close()

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client, addr in self.clients:
                if client != sender_socket:
                    try:
                        client.sendall(message.encode('utf-8'))
                    except Exception as e:
                        logging.error(f"Error broadcasting to {addr}: {e}")
                        self.remove_client(client, addr)

    def remove_client(self, client_socket, addr):
        with self.lock:
            if (client_socket, addr) in self.clients:
                self.clients.remove((client_socket, addr))
                logging.info(f"Removed client {addr}")

    def close(self):
        if self.server_socket:
            self.server_socket.close()
        logging.info("Server closed.")

if __name__ == "__main__":
    server = ChatServer()
    server.start()
