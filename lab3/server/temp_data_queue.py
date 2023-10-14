from queue import Queue
from threading import Lock
from data import Data
from time_logger import set_first_entry_time_in_second, Constants
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

            ## Just for evalution (Task 4)
            if Constants.first_entry_time_in_second == 0:
                print("*****TempDataQueue {}".format(set_first_entry_time_in_second()))