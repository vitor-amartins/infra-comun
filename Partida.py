class Partida:
    def __init__(self, id):
        self.id = id
        self.players = []
        self.count = 0

    def addPlayer(self, pl):
        self.players.append(pl)
        self.count += 1

    def getPlayers(self):
        string = "Partida " + str(self.id) + "\n"
        string += "(ID, IP)\n"
        for i in self.players:
            string += i.getPlayerInfo() + "\n"
        return string
