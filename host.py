import socket
from Match import Match
from Player import Player
    
HOST = ''
PORT = 5000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)

ID_PARTIDA = 0
ID_JOGADOR = 0
QNT_JOGADORES = 4

def updateStatusForPlayers(partida):
    msg = partida.getPlayers()
    for i in partida.players:
        dest = (i.ip, i.port)
        udp.sendto(msg.encode('utf-8'), dest)

def getMatchID():
    global ID_PARTIDA
    ID_PARTIDA += 1
    return ID_PARTIDA

def getPlayerID():
    global ID_JOGADOR
    ID_JOGADOR += 1
    return ID_JOGADOR

udp.bind(orig)
partida = None

while True:
    data, (ip, port) = udp.recvfrom(1024)
    player = Player(getPlayerID(), ip, port, data.decode())
    dest = (ip, port)
    if (partida is None):
        partida = Match(getMatchID(), QNT_JOGADORES)
        partida.addPlayer(player)
        updateStatusForPlayers(partida)
    else:
        if (partida.count < QNT_JOGADORES):
            partida.addPlayer(player)
            updateStatusForPlayers(partida)
        else:
            # msg = "Jogo está cheio"
            # udp.sendto(msg.encode('utf-8'), dest)
            # Substituir por criar outra partida
            ID_JOGADOR = 0
            player.id = getPlayerID()
            partida = Match(getMatchID(), QNT_JOGADORES)
            partida.addPlayer(player)
            updateStatusForPlayers(partida)
udp.close()

