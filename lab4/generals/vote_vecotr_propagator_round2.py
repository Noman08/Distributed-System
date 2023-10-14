import threading
from result_vector import ResultVector
from server_details import ServerDetails
from all_votes import AllVotes
from json_keys import JsonKeys
from utility import print_stack_trace, sleep
from message_queue_to_propagate import MessageQueueToPropagate
from propagate_message_info import PropagateMessageInfo
from byzantine_properties import ByzantineProperties
from byzantine_behavior import compute_byzantine_vote_round2


class VoteVectorPropagatorRound2(threading.Thread):
    def __init__(self,
                 server_details: ServerDetails,
                 result_vector: ResultVector,
                 all_votes: AllVotes,
                 is_honest: bool,
                 message_queue_to_propagate: MessageQueueToPropagate,
                 byzantine_properties: ByzantineProperties
                 ):
        super().__init__()
        self.server_details: ServerDetails = server_details
        self.result_vector: ResultVector = result_vector
        self.all_votes: AllVotes = all_votes
        self.is_honest: bool = is_honest
        self.message_queue_to_propagate: MessageQueueToPropagate = message_queue_to_propagate
        self.byzantine_properties = byzantine_properties
        self.all_votes_uri = "/vote/all_votes"
        self.running = False

    def run(self):
        self.running = True
        try:
            if self.is_honest:
                message_dict = {
                    JsonKeys.SERVER_ID: self.server_details.server_id,
                    JsonKeys.ALL_VOTES: self.result_vector.get_result_vector()
                }
                self.propagate_to_all_servers(
                    self.all_votes_uri,
                    params_dict=message_dict
                )
            else:

                # Wait if data received from all honest servers
                self.running = True
                while(self.running):
                    print(
                        "[VoteVectorPropagatorRound2]: Waiting for all honest vote")
                    sleep(1)
                    if (self.all_votes.got_all_vectors_from_loyal_servers()):
                        break

                temp_byzantine_votes = compute_byzantine_vote_round2(
                    self.byzantine_properties.no_loyal,
                    self.byzantine_properties.no_total,
                    self.byzantine_properties.on_tie
                )
                print(
                    "[VoteVectorPropagatorRound2]- temp_byzantine_votes = {}".format(temp_byzantine_votes))
                # Forward to all honest servers
                for i in range(0, len(temp_byzantine_votes)):
                    vector: [object] = temp_byzantine_votes[i]
                    message_dict = {
                        JsonKeys.SERVER_ID: self.server_details.server_id,
                        JsonKeys.ALL_VOTES: vector
                    }
                    messageObj: PropagateMessageInfo = PropagateMessageInfo(
                        self.server_details.getServerList()[i],
                        self.all_votes_uri,
                        "POST",
                        params_dict=message_dict
                    )
                    self.message_queue_to_propagate.putData(messageObj)
                self.all_votes.insert_into_vote_vectors(
                    self.server_details.server_id,
                    self.result_vector.get_result_vector()
                )
        except Exception as ex:
            print_stack_trace(ex)

        self.running = False

    def is_running(self):
        return self.running

    def propagate_to_all_servers(self, URI, req="POST", params_dict=None):
        for srv_ip in self.server_details.getServerList():
            if srv_ip != self.server_details.getServerIp():  # don't propagate to yourself
                messageObj: PropagateMessageInfo = PropagateMessageInfo(
                    srv_ip,
                    URI,
                    req,
                    params_dict
                )
                self.message_queue_to_propagate.putData(messageObj)
