from threading import Lock
from data import Data
from utility import currrent_time_secs

class Histories:
    def __init__(self):
        self.lock = Lock()
        self.history_list: [Data] = []   
        self.latest_history_entry_time = currrent_time_secs() ## Global static variable, common for all history objects

    def appendHistory(self, data: Data):
        with self.lock:
            self.latest_history_entry_time = currrent_time_secs()
            self.history_list.append(data)
    
    def clearHistory(self):
        with self.lock:
            self.history_list.clear()

    def get_history_list(self):
        with self.lock:
            return self.history_list

    def get_latest_history_entry_time(self):
        with self.lock:
            return self.latest_history_entry_time