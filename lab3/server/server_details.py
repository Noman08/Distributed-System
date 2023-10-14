from threading import Lock

class ServerDetails:
    def __init__(self, server_id, server_ip, title, servers_list):
        self.server_title = title
        self.server_id = server_id
        self.server_ip = server_ip
        self.servers_list = servers_list
        self.lock = Lock()
        

    def getServerList(self):
        return self.servers_list

    def getServerId(self):
        return self.server_id
    
    def getServerIp(self):
        return self.server_ip
    
    def changeServerTitle(self, title):
        self.server_title = title
    
    def getServerTitle(self):
        return self.server_title