class Player:
    def __init__(self, id, ip, port, name):
        self.id = id
        self.ip = ip
        self.port = port
        self.name = name

    def getPlayerInfo(self):
        return ("ID: "+str(self.id)+ "    Nome: "+ self.name + "    IP: "+str(self.ip)+"    PORT: "+str(self.port))


class inGamePlayer(Player):
    def __init__(self, id, ip, name):
        self.id = id
        self.ip = ip
        self.port = None
        self.value = None
        self.name = name
