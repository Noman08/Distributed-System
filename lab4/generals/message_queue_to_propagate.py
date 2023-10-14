from queue import Queue
from threading import Lock
from propagate_message_info import PropagateMessageInfo

class MessageQueueToPropagate:
    def __init__(self):
        self.queue = Queue()
    
    def getData(self):
        return self.queue.get()
    
    def putData(self, data: PropagateMessageInfo):
        self.queue.put(data)