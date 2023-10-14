from threading import Lock

class ServerData:
    leader_ip = None
    server_title = "Slave"
    board = dict()  # global board
    board_lock = Lock()  # Used for locking the board
    