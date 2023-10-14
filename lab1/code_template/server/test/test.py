import requests
import random
import threading
import time
from operator import itemgetter
from collections import OrderedDict

intRandomNumber = lambda: random.randint(1, 100)


class AddPostThread(threading.Thread):
    def __init__(self, threadID, name, ip, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ip = ip
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        for x in range(self.counter):
            url = "http://" + self.ip + "/board"
            key = str(self.threadID)+"-"+str(x) # 1-0
            myobj = {"id":key,"entry": "Message : " + str(self.threadID)+"-"+str(x)}
            x = requests.post(url, data=myobj)
            time.sleep(.5)
        print("Exiting " + self.name)


def runThreads(thread_id, number_of_post, ip):
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
    def __init__(self, threadID, name, ip, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ip = ip
        self.name = name
        self.counter = counter

    def run(self):
        print("ModifyThread " + self.name)
        key = str(self.threadID)+"-1" # 1-1
        url = "http://" + self.ip + "/board/"+key+"/"
        myobj = {"id":key,"entry": "Modified : " + str(self.threadID)+"-1","delete":"0"}
        x = requests.post(url, data=myobj)
        print("Exiting " + self.name)


def runModifingThreads(thread_id, number_of_post, ip):
    mthread = ModifyThread(
        thread_id, "Modifing Thread  " + ip + " # " + str(thread_id), ip, number_of_post
    )
    mthread.start()

def runThreads(thread_id, number_of_post, ip):
    mythread = AddPostThread(
        thread_id, "Thread  " + ip + " # " + str(thread_id), ip, number_of_post
    )
    mythread.start()





if __name__ == "__main__":

    runThreads(1, 5, "10.1.0.1")
    runThreads(2, 5, "10.1.0.2")
    runThreads(3, 5, "10.1.0.3")
    runThreads(4, 5, "10.1.0.4")
    runThreads(5, 5, "10.1.0.5")
    runThreads(6, 5, "10.1.0.6")
    runThreads(7, 5, "10.1.0.7")
    runThreads(8, 5, "10.1.0.8")


    runModifingThreads(1, 5, "10.1.0.1")
    runModifingThreads(2, 5, "10.1.0.2")
    runModifingThreads(3, 5, "10.1.0.3")
    runModifingThreads(4, 5, "10.1.0.4")
    runModifingThreads(5, 5, "10.1.0.5")
    runModifingThreads(6, 5, "10.1.0.6")
    runModifingThreads(7, 5, "10.1.0.7")
    runModifingThreads(8, 5, "10.1.0.8")


    # x = {1: 2, 3: 4, 4: 3, 2: 1, 10: 0}
    # sd = {'one':1,'three':3,'five':5,'two':2,'four':4}
    # # a = sorted(sd.items(), key=lambda x: x[1])  
    # a = sorted(x.keys())  
    # for x in a:
    #     print(x)
    # OrderedDict([(0, 0), (2, 1), (1, 2), (4, 3), (3, 4)])

    # dictObj = dict()
    # dictObj[0] = {'a':1}
    # dictObj[1] = {'a':4}
    # dictObj[2] = {'a':0}
    # dictObj[3] = {'a':2}
    # dictObj[4] = {'a':12}
    # dictObj[5] = {'a':3}
    # a = sorted(dictObj.items(), key=lambda x: x[1]['a'])  
    # print(a[0].values())
