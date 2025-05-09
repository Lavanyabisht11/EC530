import time
import threading
from queue import Queue
from matrix_utils import generate_large_matrix
from config import MATRIX_SIZE, FLOOD_RATE, DURATION

def flood_requests(queue):
    delay = 1 / FLOOD_RATE
    end_time = time.time() + DURATION
    while time.time() < end_time:
        a = generate_large_matrix(MATRIX_SIZE)
        b = generate_large_matrix(MATRIX_SIZE)
        queue.put((a, b))
        time.sleep(delay)
