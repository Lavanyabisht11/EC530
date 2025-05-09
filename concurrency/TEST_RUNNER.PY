from queue import Queue
import multiprocessing as mp
from task_producer import flood_requests
from queue_threaded import run_threaded
from queue_multiprocess import run_multiprocess
from config import QUEUE_SIZE

def test_threaded():
    print("Testing threaded queue...")
    queue = Queue(maxsize=QUEUE_SIZE)
    threads = run_threaded(queue)
    flood_requests(queue)
    queue.join()
    for t in threads:
        t.join()

def test_multiprocess():
    print("Testing multiprocessing queue...")
    queue = mp.JoinableQueue(maxsize=QUEUE_SIZE)
    processes = run_multiprocess(queue)
    flood_requests(queue)
    queue.join()
    for p in processes:
        p.terminate()

if __name__ == "__main__":
    test_threaded()
    test_multiprocess()
