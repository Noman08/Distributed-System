from server_details import ServerDetails
from threading import Lock


class VectorClock:
    def __init__(self, server_details: ServerDetails):
        self.server_details = server_details
        self.all_clocks = [0] * len(server_details.getServerList())
        self.lock = Lock()

    def decreaseSelfClock(self):
        with self.lock:
            decresed = self.all_clocks[self.server_details.server_id - 1] - 1
            self.all_clocks[self.server_details.server_id - 1] = decresed if (decresed >= 0) else 0

    def increaseSelfClock(self):
        with self.lock:
            self.all_clocks[self.server_details.server_id - 1] += 1
            
    def getSelfClock(self):
        with self.lock:
            return self.all_clocks[self.server_details.server_id -1]

    def update_other_server_clock(self, server_index, currentValue):
        with self.lock:
            self.all_clocks[server_index] = max(self.all_clocks[server_index], currentValue)

    def getAllClocks(self):
        with self.lock:
            return self.all_clocks
    
    def update(self, new_vector_clock):
        with self.lock:
            for index in range(0, len(new_vector_clock)):
                self.all_clocks[index] = max(self.all_clocks[index], new_vector_clock[index])
            self.all_clocks[self.server_details.server_id - 1] += 1

    def update_with_max_and_increase_self(self, new_vector_clock):
        with self.lock:
            for index in range(0, len(new_vector_clock)):
                   self.all_clocks[index] = max(self.all_clocks[index], new_vector_clock[index])
            self.all_clocks[self.server_details.server_id - 1] += 1
            self.server_details.changeServerTitle(self.all_clocks)

