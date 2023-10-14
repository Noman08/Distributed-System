import requests
import random
import threading
import time
from operator import itemgetter
from collections import OrderedDict
import json
from server.utility import is_left_array_equal_or_small_in_every_index, generate_unique_id
intRandomNumber = lambda: random.randint(1, 100)
from server.json_keys import JsonKeys

class AddPostThread(threading.Thread):
    def __init__(self, server_id, name, ip, counter):
        threading.Thread.__init__(self)
        self.server_id = server_id
        self.ip = ip
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        for x in range(1, self.counter+1):
            url = "http://" + self.ip + "/board"
            # key = str(self.threadID)+"-"+str(x) # 1-0
            # myobj = {"id":key,"entry": "Message : " + str(self.threadID)+"-"+str(x)}
            myobj = {JsonKeys.ENTRY: "Message : " + str(self.server_id)+"-"+str(x)}
            x = requests.post(url, data=myobj)
            time.sleep(.5)
        print("Exiting " + self.name)


def add_post(thread_id, number_of_post, ip):
    mythread = AddPostThread(
        thread_id, "Thread  " + ip + " # " + str(thread_id), ip, number_of_post
    )
    mythread.start()
    # time.sleep(0.1)


# def modify(element_id, modified_text, delete, ip):
#     url = "http://" + ip + "/board/" + element_id + "/"
#     myobj = {"id": element_id, "delete": delete, "entry": "Demo text "}
#     x = requests.post(url, data=myobj)
#     print(x)


class ModifyThread(threading.Thread):
    def __init__(self, server_id, name, ip):
        threading.Thread.__init__(self)
        self.server_id = server_id
        self.ip = ip
        self.name = name

    def run(self):
        print("ModifyThread " + self.name)
        key = generate_unique_id(self.server_id, 1)
        url = "http://" + self.ip + "/board/"+key+"/"
        myobj = {JsonKeys.ELEMENT_ID:key, JsonKeys.ENTRY: "Modified : " + str(self.server_id)+"_1", JsonKeys.DELETE:"0"}
        x = requests.post(url, data=myobj)
        print("Exiting " + self.name)

## Modify first entry of a server
def runModifingThreads(thread_id, ip):
    mthread = ModifyThread(
        thread_id, "Modifing Thread  " + ip + " # " + str(thread_id), ip
    )
    mthread.start()



if __name__ == "__main__":

    add_post(1, 5, "10.1.0.1")
    add_post(2, 4, "10.1.0.2")
    add_post(3, 4, "10.1.0.3")
    add_post(4, 4, "10.1.0.4")
    add_post(5, 4, "10.1.0.5")
    # add_post(8, 5, "10.1.0.8")


    
    # runModifingThreads(1, "10.1.0.1")
    # runModifingThreads(2, "10.1.0.2")
    # runModifingThreads(3, "10.1.0.3")
