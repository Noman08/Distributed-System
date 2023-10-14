import threading
# from server_data import ServerData
from server_details import ServerDetails
from distributed_board import DistributedBoard
from vector_clock import VectorClock
from temp_data_queue import TempDataQueue
from data import Data
from action_type import ActionType
from utility import generate_unique_id, print_stack_trace
from json_keys import JsonKeys
from historires import Histories
from propagate_message_info import PropagateMessageInfo
from message_queue_to_propagate import MessageQueueToPropagate


class ClientDataProcessor(threading.Thread):
    def __init__(self, server_details: ServerDetails, histories: Histories, vector_clock: VectorClock, temp_data_queue: TempDataQueue, message_queue_to_propagate: MessageQueueToPropagate):
        super().__init__()
        self.server_details = server_details
        self.histories = histories
        self.running = True
        self.vector_clock = vector_clock
        self.temp_data_queue = temp_data_queue
        self.message_counter = 0
        self.message_queue_to_propagate = message_queue_to_propagate

    def run(self):
        print("[ClientDataProcessor]: started")
        while(self.running):
            try:
                data: Data = self.temp_data_queue.queue.get()  # Wait if empty
                # It's mandatory to create an unique id for each message while adding new message
                if(data.action_type == ActionType.ADD):
                    self.message_counter += 1
                    data.element_id = generate_unique_id(
                        self.server_details.getServerId(), self.message_counter)

                if(data.text != None and len(data.element_id) > 0):
                    message_with_id = {
                        JsonKeys.ELEMENT_ID: data.element_id,
                        JsonKeys.ENTRY: data.text,
                        JsonKeys.VECTOR_CLOCK: data.vector_clock,
                        JsonKeys.ACTION_TYPE: int(data.action_type),
                        JsonKeys.SERVER_ID: self.server_details.server_id
                    }
                    self.histories.appendHistory(data)
                    self.propagate_to_all_servers(
                        "/propagated_data", "POST", message_with_id)
                else:
                    print("[ClientDataProcessor: Error] text = {}, element_id = {}, action_type = {}".format(
                        data.text, data.element_id, data.action_type))

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
                # success = contact_another_server(
                #     srv_ip, URI, req, params_dict)
                # if not success:
                #     print("[ClientDataProcessor: propagate_to_all_servers : WARNING ] {}".format(srv_ip))
