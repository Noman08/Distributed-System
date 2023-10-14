import numpy as np
from server_details import ServerDetails
from byzantine_properties import ByzantineProperties


class ResultVector:
    def __init__(self,
                 server_details: ServerDetails,
                 byzantine_properties: ByzantineProperties):
        self.server_details = server_details
        self.number_of_servers = len(self.server_details.getServerList())
        self.result_vector = [None] * self.number_of_servers
        self.vote_counter = 0
        self.byzantine_properties: ByzantineProperties = byzantine_properties
        self.end_result: str = "None"

    def reset_result_vector(self):
        # self.result_vector = np.empty(
        #     len(self.server_details.getServerList()),
        #     dtype=object
        # )
        self.vote_counter = 0

    def insert_into_result_vector(self, server_id: int, is_attack: bool):
        self.result_vector[server_id - 1] = is_attack
        self.vote_counter += 1

    def got_all_vote_from_loyal_servers(self):
        return True if (self.vote_counter == (self.byzantine_properties.no_loyal)) else False

    def got_vote_from_all_servers(self):
        return True if (self.vote_counter == (self.number_of_servers)) else False

    def get_result_vector(self):
        return self.result_vector


if __name__ == "__main__":
    server_details = ServerDetails(
        4, "", "", ["10.1.0.1", "10.1.0.2", "10.1.0.3", "10.1.0.4"])
    # res = ResultVector(server_details)
    # res.insert_into_result_vector(1, False)
    # res.insert_into_result_vector(2, True)
    # res.insert_into_result_vector(3, False)
    # res.insert_into_result_vector(4, False)
    # print(res.got_vote_from_all_servers())
