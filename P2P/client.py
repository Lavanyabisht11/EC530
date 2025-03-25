import socket
import threading
import sys
import logging

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            logging.info(f"Connected to server at {self.host}:{self.port}")
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True  # Allow the main thread to exit even if this thread is running
            receive_thread.start()
            self.send_messages()
        except ConnectionRefusedError:
            logging.error("Could not connect to the server. Make sure the server is running.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()
                logging.info("Disconnected from the server.")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    logging.info("Disconnected from the server.")
                    break
                message = data.decode('utf-8').strip()
                print(f"Received: {message}")
            except ConnectionResetError:
                logging.info("Server closed the connection.")
                break
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
                break

    def send_messages(self):
        while True:
            try:
                message = input("> ")
                if message.lower() == 'quit':
                    break
                self.client_socket.sendall(message.encode('utf-8'))
            except BrokenPipeError:
                logging.error("Connection to server broken.")
                break
            except KeyboardInterrupt:
                logging.info("Quitting the chat.")
                break
            except Exception as e:
                logging.error(f"Error sending message: {e}")
                break

if __name__ == "__main__":
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
        client = ChatClient(host, port)
        client.connect()
    else:
        print("Usage: python client.py <server_ip> <server_port>")
        print("Example: python client.py localhost 12345")
