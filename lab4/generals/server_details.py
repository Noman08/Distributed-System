from threading import Lock

class ServerDetails:
    def __init__(self, server_id:int, server_ip:str, title:str, servers_list: [str]):
        self.server_title:str = title
        self.server_id: int = server_id
        self.server_ip: str = server_ip
        self.servers_list: [str] = servers_list
        

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