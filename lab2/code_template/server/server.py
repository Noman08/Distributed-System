# coding=utf-8
import argparse
import json
import sys
from threading import Lock, Thread
import time
import traceback
import bottle
from bottle import Bottle, request, template, run, static_file
import requests
import random
from leader_election import Election
from data_processor import DataProcessor
from server_data import ServerData
# ------------------------------------------------------------------------------------------------------


def current_milli_time(): return int(round(time.time() * 1000))
def intRandomNumber(): return random.randint(1, 100)
def current_time_in_seconds(): return int(round(time.time()))


prapagation_delay = 5  # in second


class Blackboard:
    def __init__(self):
        self.content = ""
        self.lock = Lock()  # use lock when you modify the content

    def get_content(self):
        with self.lock:
            cnt = self.content
        return cnt

    def set_content(self, new_content):
        with self.lock:
            self.content = new_content
        return

# ------------------------------------------------------------------------------------------------------


class Server(Bottle):

    def __init__(self, ID, IP, servers_list):
        super(Server, self).__init__()
        self.blackboard = Blackboard()
        self.id = int(ID)
        self.ip = str(IP)
        self.servers_list = servers_list
        # list all REST URIs
        # if you add new URIs to the server, you need to add them here
        self.route("/", callback=self.index)
        self.get("/board", callback=self.get_board)
        self.post("/", callback=self.post_index)

        # we give access to the templates elements
        self.get("/templates/<filename:path>", callback=self.get_template)
        self.post("/board", callback=self.add_on_board)
        self.post("/board/<element_id>/", callback=self.modify_delete)
        self.post("/election", callback=self.election)
        self.post("/leader", callback=self.leader)
        self.get("/sync",callback=self.sync)
        self.time_in_seconds_of_first_message = 0
        self.time_in_seconds_of_last_message = 0

        # You can have variables in the URI, here's an example
        # self.post('/board/<element_id:int>/', callback=self.post_board) where post_board takes an argument (integer) called element_id
        # self.board = dict()  # global board
        # self.board_lock = Lock()  # Used for locking the board
        
        ServerData.leader_ip = self.servers_list[len(
            self.servers_list)-1]  # last ip as leader
        
        self.leader_id = len(self.servers_list)
        self.electionThread = None
        self.dataprocessThread = None
        

    def get_board_items(self):
        with ServerData.board_lock:
            board = ServerData.board
            return board

    def delete_key(self, key):
        print("[DELETE] " + str(key))
        with ServerData.board_lock:
            try:
                del ServerData.board[key]
            except KeyError as ex:
                print("[ERROR] " + str(ex))
            return

    def get_value(self, key):
        with ServerData.board_lock:
            value = ServerData.board[key]
            return value

    def insert_or_update_in_board(self, new_content, e_id):
        new_kew = e_id
        with ServerData.board_lock:
            # if len(new_kew.strip()) == 0:
            #     c_time = current_milli_time()
            #     new_kew = (
            #         str(c_time) + "_" + str(e_id)
            #     )  # id = 23423432_1 , (there same data in same mili second in all server, that's why I used _ and server id)
            self.blackboard.set_content(new_content)
            
            ServerData.board[new_kew] = self.blackboard.get_content()
            if(len(ServerData.board)) == 1 :
                self.time_in_seconds_of_first_message = current_time_in_seconds()
            elif(len(ServerData.board) == 40):
                print("Total time = {}".format((current_time_in_seconds() - self.time_in_seconds_of_first_message)))

        return new_kew

    def do_parallel_task(self, method, args=None):
        # create a thread running a new task
        # Usage example: self.do_parallel_task(self.contact_another_server, args=("10.1.0.2", "/index", "POST", params_dict))
        # this would start a thread sending a post request to server 10.1.0.2 with URI /index and with params params_dict
        thread = Thread(target=method, args=args)
        thread.daemon = True
        thread.start()

    def do_parallel_task_after_delay(self, delay, method, args=None):
        # create a thread, and run a task after a specified delay
        # Usage example: self.do_parallel_task_after_delay(10, self.start_election, args=(,))
        # this would start a thread starting an election after 10 seconds
        thread = Thread(
            target=self._wrapper_delay_and_execute, args=(delay, method, args)
        )
        thread.daemon = True
        thread.start()

    def _wrapper_delay_and_execute(self, delay, method, args):
        time.sleep(delay)  # in sec
        method(*args)

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

    def propagate_to_all_servers(self, URI, req="POST", params_dict=None):
        for srv_ip in self.servers_list:
            if srv_ip != self.ip:  # don't propagate to yourself
                success = self.contact_another_server(
                    srv_ip, URI, req, params_dict)
                if not success:
                    print("[WARNING ]Could not contact server {}".format(srv_ip))

    def start_leader_election_thread(self):
        if(self.electionThread == None or (not self.electionThread.is_alive())):
            print("+=====start_leader_electionhread==================")
            electionThread = Election(self.ip, self.id, self.servers_list)
            electionThread.start()

    def start_data_processing_thread(self):
        if(self.dataprocessThread == None or not self.dataprocessThread.isRunning()):
            print("+===============start_data_processing_thread=====================")
            self.dataprocessThread = DataProcessor(
                self.id, self.ip, self.servers_list)
            self.dataprocessThread.start()

    # route to ('/')

    def index(self):
        # we must transform the blackboard as a dict for compatiobility reasons
        # board = dict()
        board = self.get_board_items()
        return template(
            "server/templates/index.tpl",
            board_title="Server {} ({})".format(self.id, self.ip),
            board_dict=board.items(),
            server_title = ServerData.server_title,
            members_name_string="Faiz Ahmed & Md Abu Noman Majumdar",
        )

    # get on ('/board')
    def get_board(self):
        # we must transform the blackboard as a dict for compatibility reasons
        # board = dict()
        board = self.get_board_items()
        return template(
            "server/templates/blackboard.tpl",
            board_title="Server {} ({})".format(self.id, self.ip),
            server_title = ServerData.server_title,
            board_dict=board.items(),
        )

    # post on ('/')
    def post_index(self):
        try:
            # we read the POST form, and check for an element called 'entry'
            new_entry = request.forms.get("entry")

            print("Received: {}".format(new_entry))
        except Exception as e:
            print("[ERROR] " + str(e))

    # post on ('/board')
    def add_on_board(self):
        try:
            text = request.forms.get("entry")

            if "id" in request.forms:  # got from Leader
                self.insert_or_update_in_board(text, request.forms.get("id"))
            else:
                if ServerData.leader_ip == self.ip:
                    self.start_data_processing_thread()
                    self.dataprocessThread.pushData(text)
                else:
                    # If Coordinator does not response start election
                    success = self.contact_another_server(
                        ServerData.leader_ip, "/board", "POST", {"entry": text})
                    print("leader : {} , text : {} , success {}".format(
                        ServerData.leader_ip, text, success))
                    if not success: # start election
                        print("Running election")
                        self.start_leader_election_thread()
        except Exception as ex:
            print("[ERROR] " + str(ex))

    # post on ('/election')
    def election(self):
        try:
            self.start_leader_election_thread()
            print("found election from : {}".format(request.forms.get("l_ip")))
        except Exception as ex:
            print("[ERROR] " + str(ex))

    # post on ('/leader')
    def leader(self):
        try:
            ServerData.leader_ip = request.forms.get("l_ip")
            self.leader_id = request.forms.get("l_id")
            print("leader_ip=> {}".format(ServerData.leader_ip))
            if(ServerData.leader_ip != self.ip):
                ServerData.server_title = "Slave"
                if self.dataprocessThread != None:
                    print("Stopping processor thread")
                    self.dataprocessThread.stop()
                    self.dataprocessThread = None
                    
                

            print(True)
        except Exception as ex:
            print("[ERROR] " + str(ex))

    def modify_delete(self, element_id):
        try:
            print("modify_delete ", element_id)
            isDelete = request.forms.get("delete", type=int)
            entry = request.forms.get("entry")
            print("e_id {} isDelete {} entry {} ".format(
                element_id, isDelete, entry))
            if element_id in self.get_board_items():
                if isDelete == 1:
                    self.delete_key(element_id)
                else:
                    self.insert_or_update_in_board(entry, element_id)
            else:
                print("[ERROR] No Entry")

            # Propagate upadate to other servers, "propagated" flag is used to tackle retransmission again from server
            if not "propagated" in request.forms:
                self.do_parallel_task_after_delay(
                    prapagation_delay,
                    self.propagate_to_all_servers,
                    args=(
                        "/board/" + element_id + "/",
                        "POST",
                        {
                            "entry": entry,
                            "id": element_id,
                            "delete": isDelete,
                            "propagated": 1,
                        },
                    ),
                )
        except Exception as identifier:
            print("[ERROR] " + str(identifier))
    
    # get "/sync"
    def sync(self):
        return self.get_board_items()


    def get_template(self, filename):
        return static_file(filename, root="./server/templates/")
    

# ------------------------------------------------------------------------------------------------------


def main():
    PORT = 80
    parser = argparse.ArgumentParser(
        description="Your own implementation of the distributed blackboard"
    )
    parser.add_argument(
        "--id", nargs="?", dest="id", default=1, type=int, help="This server ID"
    )
    parser.add_argument(
        "--servers",
        nargs="?",
        dest="srv_list",
        default="10.1.0.1,10.1.0.2",
        help="List of all servers present in the network",
    )
    args = parser.parse_args()
    server_id = args.id
    server_ip = "10.1.0.{}".format(server_id)
    servers_list = args.srv_list.split(",")
    # lead?er_ip = servers_list[len(servers_list)-1]

    try:
        server = Server(server_id, server_ip, servers_list)
        if(server_id == len(servers_list)):
            time.sleep(3)  # for starting all servers
            ## Starting election at starting 
            election = Election(server_ip, server_id, servers_list)
            election.start()
        bottle.run(server, host=server_ip, port=PORT)
    except Exception as e:
        print("[ERROR] " + str(e))


# ------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
