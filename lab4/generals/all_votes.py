from server_details import ServerDetails
from threading import Lock
from byzantine_properties import ByzantineProperties


class AllVotes:
    def __init__(self,
                 server_details: ServerDetails,
                 byzantine_properties: ByzantineProperties
                 ):
        self.server_details: ServerDetails = server_details
        self.no_of_servers = len(server_details.getServerList())
        self.byzantine_properties: ByzantineProperties = byzantine_properties
        self.vote_vectors = [
            [None]*self.no_of_servers for i in range(self.no_of_servers)
        ]
        self.counter = 0
        self.lock = Lock()

    def insert_into_vote_vectors(self, server_id, vector: [object]):
        with self.lock:
            self.vote_vectors[server_id - 1] = vector
            self.counter += 1

    def get_vote_vectors(self):
        return self.vote_vectors

    def got_all_vectors_from_loyal_servers(self):
        return True if (self.counter == self.byzantine_properties.no_loyal) else False

    def got_vectors_from_all_servers(self):
        return True if (self.counter == self.no_of_servers) else False

    def reset(self):
        self.counter = 0


if __name__ == '__main__':
    server_details = ServerDetails(
        4, "", "", ["10.1.0.1", "10.1.0.2", "10.1.0.3", "10.1.0.4"])
    # all_votes = AllVotes(server_details)
    # all_votes.insert_into_vote_vectors(1, [True, False, None, True])
    # all_votes.insert_into_vote_vectors(2, [True, None, None, True])
    # all_votes.insert_into_vote_vectors(3, [True, True, None, True])
    # all_votes.insert_into_vote_vectors(4, [True, None, None, True])

    # print(all_votes.got_all_vectors_from_loyal_servers())
