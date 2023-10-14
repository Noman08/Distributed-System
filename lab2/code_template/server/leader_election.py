#!/usr/bin/python3
import socket
import threading
import time
import random
import requests
from server_data import ServerData


class Election(threading.Thread):
    def __init__(self, server_ip, server_id, server_list):
        super().__init__()
        self.server_id = server_id
        self.server_ip = server_ip
        self.server_list = server_list
     
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

    def run(self):
        # while(True):
        print("============== Running Election Thread===========================")
        time.sleep(1)
        print(self.server_list)
        # print("Leader IP : "+ ServerData.leader_ip)
        elected = True
        no_of_servers = len(self.server_list)
        if(no_of_servers != self.server_id):  ## started from last index
            # for i in range(self.server_id-1, len(self.server_list)-1):
            for i in range(no_of_servers-1, self.server_id, -1):
                ip = self.server_list[i]
                print("send election to :"+ip)
                messge = {"l_id": self.server_id,
                          "l_ip": self.server_ip}
                success = self.contact_another_server(
                    ip, "/election", "POST", messge)
                if(success):
                    elected = False
                    break
        if(elected):
            print("=================I am the Coordinator=========== \nid: {} , ip: {}".format(self.server_id,self.server_ip))
            ServerData.leader_ip = self.server_ip
            ServerData.server_title = "Master"
            ## Fetch previous board data from server 1, for synchronization purpose##
            try:
                response = requests.get("http://{}{}".format(self.server_list[0], "/sync"), data={})
                if response.status_code == 200:
                    board = response.json()
                    for key,value in board.items():
                        ServerData.board[key] = value

            except Exception as identifier:
                print("[ERROR] " + str(identifier))
            ## Notify other servers with self IP as leader
            for i in range(len(self.server_list)):
                ip = self.server_list[i]
                if self.server_ip != ip:
                    messge = {"l_id": self.server_id,
                              "l_ip": self.server_ip, "entry": "test"}
                    success = self.contact_another_server(
                        ip, "/leader", "POST", messge)
                    print(" Leader selected sent =>{} , response : {}".format(
                        ip, success))

    def gerServerList(self):
        return self.server_list