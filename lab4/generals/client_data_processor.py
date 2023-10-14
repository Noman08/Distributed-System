import threading
# from server_data import ServerData
from server_details import ServerDetails
from temp_data_queue import TempDataQueue
from data import Data
from utility import generate_unique_id, print_stack_trace
from json_keys import JsonKeys
from propagate_message_info import PropagateMessageInfo
from message_queue_to_propagate import MessageQueueToPropagate


class ClientDataProcessor(threading.Thread):
    def __init__(self, server_details: ServerDetails, temp_data_queue: TempDataQueue, message_queue_to_propagate: MessageQueueToPropagate):
        super().__init__()
        self.server_details = server_details
        self.running = True
        self.temp_data_queue = temp_data_queue
        self.message_counter = 0
        self.message_queue_to_propagate = message_queue_to_propagate

    def run(self):
        print("[ClientDataProcessor]: started")
        while(self.running):
            try:
                data: Data = self.temp_data_queue.queue.get()  # Wait if empty

                if(data.propagate == True):
                    message_with_id = {
                        JsonKeys.SERVER_ID: data.server_id,
                        JsonKeys.IS_ATTACK: data.is_attack
                    }
                    uri : str = "/vote/attack" if data.is_attack else "/vote/retreat"
                    self.propagate_to_all_servers(uri, "POST", message_with_id)
                else:
                    print("[ClientDataProcessor: Error] is_attack = {}, server_id = {}".format(
                        data.is_attack, data.server_id))

            except Exception as identifier:
                print_stack_trace(identifier)

    def stop(self):
        self.running = False

    def isRunning(self):
        return self.running

    def propagate_to_all_servers(self, URI, req="POST", params_dict=None):
        for srv_ip in self.server_details.getServerList():
            if srv_ip != self.server_details.getServerIp():  # don't propagate to yourself
                messageObj: PropagateMessageInfo = PropagateMessageInfo(
                    srv_ip, URI, req, params_dict)
                self.message_queue_to_propagate.putData(messageObj)
