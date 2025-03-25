import unittest
import socket
import threading
import time
from server.server import ChatServer

class TestChatServer(unittest.TestCase):

    def setUp(self):
        self.server = ChatServer(host='localhost', port=12346)  # Use a different port for testing
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(0.1)  # Give the server some time to start

    def tearDown(self):
        self.server.close()
        self.server_thread.join(timeout=1)

    def test_server_starts_and_accepts_connection(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(('localhost', 12346))
            self.assertTrue(True, "Successfully connected to the server.")
        except ConnectionRefusedError:
            self.fail("Could not connect to the server.")
        finally:
            client_socket.close()

    def test_server_broadcasts_message(self):
        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client1.connect(('localhost', 12346))
            client2.connect(('localhost', 12346))

            client1.sendall("Hello from client 1".encode('utf-8'))
            time.sleep(0.1)
            received_data = client2.recv(1024).decode('utf-8')
            self.assertIn("Hello from client 1", received_data)

        except Exception as e:
            self.fail(f"An error occurred during the test: {e}")
        finally:
            client1.close()
            client2.close()

if __name__ == '__main__':
    unittest.main()
