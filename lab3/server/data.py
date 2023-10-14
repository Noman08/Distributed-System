import math
from  action_type import ActionType

class Data:
    def __init__(self, data: str, element_id: str, action_type: ActionType, server_id:int):
        self.text: str = data
        self.element_id: str = element_id
        self.action_type: ActionType = action_type
        self.vector_clock: [int] = []
        self.server_id: int = server_id
        self.vector_sum: int = math.inf

    def set_vector_clock(self, vector_clock):
        self.vector_clock = vector_clock
        self.vector_sum = sum(vector_clock)


    