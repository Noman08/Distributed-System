class Data:
    def __init__(self, server_id: int,  is_attact: bool = True, propagate: bool = True):
        self.is_attack: bool = is_attact
        self.server_id: int = server_id
        self.propagate: bool = propagate