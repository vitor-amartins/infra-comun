class Partida:
    def __init__(self, id, maxP):
        self.id = id
        self.players = []
        self.count = 0
        self.maxP = maxP

    def addPlayer(self, pl):
        self.players.append(pl)
        self.count += 1

    def getPlayers(self):
        string = "Partida " + str(self.id) + " | Jogadores necessários: " + str(self.maxP) + "\n"
        for i in self.players:
            string += i.getPlayerInfo() + "\n"
        return string
