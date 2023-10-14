import threading
from byzantine_behavior import compute_byzantine_vote_round1
from byzantine_properties import ByzantineProperties
from server_details import ServerDetails
from result_vector import ResultVector
from utility import sleep
from message_queue_to_propagate import MessageQueueToPropagate
from propagate_message_info import PropagateMessageInfo
from json_keys import JsonKeys


class ByzantineRound1(threading.Thread):
    def __init__(self,
                 result_vector: ResultVector,
                 server_details: ServerDetails,
                 byzantine_properties: ByzantineProperties,
                 message_queue_to_propagate: MessageQueueToPropagate):
        super().__init__()
        self.result_vector: ResultVector = result_vector
        self.server_details: ServerDetails = server_details
        self.running = False
        self.byzantine_properties: ByzantineProperties = byzantine_properties
        self.message_queue_to_propagate: MessageQueueToPropagate = message_queue_to_propagate

    def run(self):
        self.running = True
        while(self.running):
            print("[ByzantineRound1]: Waiting for all honest vote")
            sleep(1)
            if (self.result_vector.got_all_vote_from_loyal_servers()):
                break

        byzantine_result = compute_byzantine_vote_round1(
            self.byzantine_properties.no_loyal, self.byzantine_properties.no_total, self.byzantine_properties.on_tie)
        print("[ByzantineRound1] - byzantine_result {}".format(byzantine_result))
        for i in range(0, len(byzantine_result)):
            attack = byzantine_result[i]
            if i != (self.server_details.server_id - 1):
                message_with_id = {
                    JsonKeys.SERVER_ID: self.server_details.server_id
                }
                uri = "/vote/attack"
                if not attack:
                    uri = "/vote/retreat"

                messageObj: PropagateMessageInfo = PropagateMessageInfo(
                    self.server_details.getServerList()[i],
                    uri,
                    "POST",
                    message_with_id
                )
                self.message_queue_to_propagate.putData(messageObj)

            else:
                self.result_vector.insert_into_result_vector(
                    self.server_details.server_id,
                    attack
                )
        self.running = False

    def is_running(self):
        return self.running
