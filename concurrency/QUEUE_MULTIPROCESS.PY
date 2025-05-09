import multiprocessing as mp
import numpy as np
from config import QUEUE_SIZE

def worker(queue):
    while True:
        try:
            a, b = queue.get(timeout=3)
            result = np.matmul(a, b)
            queue.task_done()
        except Exception:
            break

def run_multiprocess(queue, num_processes=4):
    processes = []
    for _ in range(num_processes):
        p = mp.Process(target=worker, args=(queue,))
        p.start()
        processes.append(p)
    return processes
