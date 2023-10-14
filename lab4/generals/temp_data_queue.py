from queue import Queue
from threading import Lock
from data import Data
class TempDataQueue:
    def __init__(self):
        self.queue = Queue()
        self.lock = Lock()
    
    def getData(self):
        with self.lock:
            return self.queue.get()
    
    def putData(self, data: Data):
        with self.lock:
            self.queue.put(data)
