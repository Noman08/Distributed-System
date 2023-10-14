
class PropagateMessageInfo:

    def __init__(self, ip: str, url: str, method: str, params_dict: None):
        self.ip: str = ip
        self.url: str = url
        self.method: str = method
        self.params_dict = params_dict
        self.retry_count: int = 0

    def set_retry_count(self, count: int):
        self.retry_count = count
