import socket
from Player import inGamePlayer

HOST = '172.22.79.112'
PORT = 5000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

def choseNumber():
    print("Escolha um número de 1 a 10:")
    number = input()
    while(int(number) < 1 or int(number) > 10):
        print("Escolha um número de 1 a 10:")
        number = input()
    return number

def getPlayers(info, peers):
    allPlayers = []
    j = 1
    while (j <= peers):
        i = info[j].find("ID: ") + len("ID: ")
        str1 = ''
        while(info[j][i] != ' '):
            str1 += info[j][i]
            i += 1
        i = info[j].find("IP: ") + len("IP: ")
        str2 = ''
        while(info[j][i] != ' '):
            str2 += info[j][i]
            i += 1

        allPlayers.append(inGamePlayer(str1, str2))
        j += 1
        
    return allPlayers

def getIP(info):
    i = info.find("IP: ") + len("IP: ")
    str1 = ''
    while(info[i] != ' '):
        str1 += info[i]
        i += 1
    return str1

PORT_RCV_VALUE = 31245
KNOWN_VALUES = 1
MY_IP = None
valueByIP = []

def enviarValor(valor, ips):
    msg = str(valor)
    for i in ips:
        if (i != MY_IP):
            destPlayer = (i, PORT_RCV_VALUE)
            udp.sendto(msg.encode('utf-8'), destPlayer)

def receberValor():
    global KNOWN_VALUES
    while (KNOWN_VALUES < PEERS):
        valor, address = udp.recvfrom(2048)
        ip, port = address
        if (valueByIP[ip] == None):
            valueByIP[ip] = int(valor)
            KNOWN_VALUES += 1


print("Deseja entrar no jogo? (Y / N)")
msg = input()

if (msg == 'Y'):
    udp.sendto(msg.encode(), dest)

while True:
    
    serverMsg, serverAddress = udp.recvfrom(2048)
    msg = serverMsg.decode()
    print(msg)
    PEERS = int(msg[msg.find("Jogadores necessários: ") + len("Jogadores necessários: ")])
    info = msg.split('\n')

    if(MY_IP == None):
        MY_IP = getIP(info[len(info)-2])
    
    if (len(info) - 2 == PEERS):
        print("Link Start")
        allPlayers = getPlayers(info, PEERS)
        valueByIP[MY_IP] = choseNumber()
        # Envia o seu valor aos outros jogadores
        # Recebe os valores dos outros jogadores

input()
udp.close()