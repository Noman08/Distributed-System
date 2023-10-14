import threading
import time
import queue
import requests
from server_data import ServerData


def current_milli_time(): return int(round(time.time() * 1000))


class DataProcessor(threading.Thread):
    def __init__(self, server_id, server_ip, servers_list):
        super().__init__()
        self.server_id = server_id
        self.server_ip = server_ip
        self.servers_list = servers_list
        self.queue = queue.Queue()
        self.running = True
        self.push_lock = threading.Lock()

    def run(self):
        while(self.running):
            try:
                message = self.queue.get()  # Wait if empty
                message_id = "{}_{}".format(current_milli_time(),self.server_id)
                message_with_id = {"id": message_id,
                                   "entry": message}
                # self.data_dictionary[self.message_id] = message
                print("Propagating id: {}".format(message_id))
                ServerData.board[message_id] = message
                for i in range(len(self.servers_list)):
                    ip = self.servers_list[i]
                    if(ip != self.server_ip):
                        self.contact_another_server(
                            ip, "/board", "POST", message_with_id)
            except Exception as identifier:
                print("[ERROR] " + str(identifier))
        print("** Data processor Stopped ****")

    def contact_another_server(self, srv_ip, URI, req="POST", params_dict=None):
        # Try to contact another serverthrough a POST or GET
        # usage: server.contact_another_server("10.1.1.1", "/index", "POST", params_dict)
        success = False
        try:
            if "POST" in req:
                res = requests.post(
                    "http://{}{}".format(srv_ip, URI), data=params_dict)
            elif "GET" in req:
                res = requests.get("http://{}{}".format(srv_ip, URI))
            # result can be accessed res.json()
            if res.status_code == 200:
                success = True
        except Exception as e:
            print("[ERROR] " + str(e))
        return success

    def stop(self):
        self.running = False

    def isRunning(self):
        return self.running

    def pushData(self, data):
        with self.push_lock:
            self.queue.put(data)
