from threading import Lock
from data import Data


class DistributedBoard:
    def __init__(self, server_details):
        self.lock = Lock()
        self.board_data = dict()

    def delete_key(self, key):
        print("[DELETE] " + str(key))
        with self.lock:
            try:
                del self.board_data[key]
            except KeyError as ex:
                print("[ERROR] " + str(ex))
            return

    def delete_if_exist(self, key):
        print("[DELETE if exist] " + str(key))
        with self.lock:
            if key in self.board_data:
                del self.board_data[key]
                return True
            return False

    def get_board_items(self):
        with self.lock:
            board = self.board_data
            return board

    def get_value(self, key):
        with self.lock:
            value = self.board_data[key]
            return value

    def add_on_board(self, dataObj: Data):
        with self.lock:
            self.board_data[dataObj.element_id] = dataObj
            return True
        return False

    def update_text_from_borad(self, dataObj: Data):
        with self.lock:
            if dataObj.element_id in self.board_data:
                self.board_data[dataObj.element_id].text = dataObj.text
                return True
        return False
