import requests
import random
import threading
import time
from queue import Queue
from server.distributed_board import DistributedBoard

def getLastNobjectsFromDictionaries():
    pass


if __name__ == "__main__":
    print("Main")
    print(round(3.50))

    queue = Queue()
    queue.put(1)
    queue.put(2)
    queue.put(3)
    queue.put(4)

    while(True):
        time.sleep(2)
        value = queue.get()
        if(value % 2 == 0):
            queue.put(value)

        print(value)
