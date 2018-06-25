class Player:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port

    def getPlayerInfo(self):
        return ("ID: "+str(self.id)+"\nIP: "+str(self.ip)+"\nPORT: "+str(self.port)+"\n")
