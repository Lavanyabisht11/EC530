import threading
import numpy as np
from queue import Queue
from config import QUEUE_SIZE

def worker(queue):
    while True:
        try:
            a, b = queue.get(timeout=3)
            result = np.matmul(a, b)  # Simulate heavy API call
            queue.task_done()
        except Exception:
            break

def run_threaded(queue, num_threads=4):
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(queue,))
        t.start()
        threads.append(t)
    return threads
