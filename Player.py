class Player:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port

    def getPlayerInfo(self):
        return ("ID: "+str(self.id)+"    IP: "+str(self.ip)+"    PORT: "+str(self.port))
