import socket
import threading, time
from Player import inGamePlayer

HOST = '172.22.46.63'
PORT = 5000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

PORT_RCV_VALUE = 6000
PORT_SND_VALUE = 6000
KNOWN_VALUES = 1
MY_IP = None
allPlayers = []

ATTEMPTS = 3
TIMEOUT_SEND = 5
TIMEOUT_RCV = 60

threadSend = None
threadRcv = None

def choseNumber():
    print("Você tem 60 segundos para escolher, após isso será considerado AFK e perderá a partida")
    print("Escolha um número de 0 a 10:")
    number = input()
    while(int(number) < 0 or int(number) > 10):
        print("Escolha um número de 0 a 10:")
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

def setValueOnIP(ip, value):
    global allPlayers
    for i in allPlayers:
        if (i.ip == ip):
            i.value = value
            break

def getValueOnIP(ip):
    global allPlayers
    for i in allPlayers:
        if (i.ip == ip):
            return i.value

def getListIP():
    global allPlayers
    ips = []
    for i in allPlayers:
        ips.append(i.ip)
    return ips

def getPeers(msg):
    return int(msg[msg.find("Jogadores necessários: ") + len("Jogadores necessários: ")])

def removePlayerByIP(ipToRemove):
    global allPlayers
    index = 0
    for i in range(len(allPlayers)):
        if (allPlayers[i].ip == ipToRemove):
            del allPlayers[i]
            index = i
            break
    decrementIDFromIndex(index)

def decrementIDFromIndex(index):
    for i in range(index, len(allPlayers)):
        allPlayers[i].id = str(int(allPlayers[i].id) - 1)

def getIPWithoutValue():
    ips = []
    for i in allPlayers:
        if(i.value == None):
            ips.append(i.ip)
    return ips

def sendValue(valor, ips):
    udpSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSend.settimeout(TIMEOUT_SEND)
    msg = str(valor)
    for i in ips:
        attemptsTried = 0
        successful = False
        while (attemptsTried < ATTEMPTS and not successful):
            if (i != MY_IP): # Evita que envie para si mesmo
                destPlayer = (i, PORT_SND_VALUE)
                # print("Enviando " + msg + " para " + i + " na porta " + str(PORT_SND_VALUE) + "\n")
                udpSend.sendto(msg.encode('utf-8'), destPlayer)
                # print("Enviado")
                # Aguarda ACK
                try:
                    serverMsg, serverAddress = udpSend.recvfrom(2048)
                    msg = serverMsg.decode()
                    if (msg == "OK"):
                        # print("Sucesso")
                        successful = True
                    else:
                        attemptsTried += 1
                except socket.timeout:
                    attemptsTried += 1
                    continue
            else:
                successful = True
        if not successful:
            removePlayerByIP(i)
    udpSend.close()

def receiveValue():
    global KNOWN_VALUES
    orig = (MY_IP, PORT_RCV_VALUE)
    udpRcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpRcv.settimeout(TIMEOUT_RCV)
    udpRcv.bind(orig)
    while (KNOWN_VALUES < len(allPlayers)): # Caso não conheça o valor de todos os jogadores, aguarda recebê-los 
        # print("Esperando: " + MY_IP + ", " + str(PORT_RCV_VALUE))
        # Espera receber um valor
        try:
            valor, address = udpRcv.recvfrom(2048)
            ip, port = address
            valor = valor.decode()
            # Se ainda não tinha o valor recebido, salva este valor no ip respectivo
            if (getValueOnIP(ip) == None):
                setValueOnIP(ip, int(valor))
                KNOWN_VALUES += 1
            print(ip, valor)
            # Envia um ACK confirmando o recebimento do valor daquele ip
            msg = "OK"
            udpRcv.sendto(msg.encode('utf-8'), address)
        except socket.timeout:
            ips = getIPWithoutValue()
            for i in ips:
                removePlayerByIP(i)
            continue
    udpRcv.close()

def getWinner():
    global allPlayers
    sum = 0
    for i in allPlayers:
        sum += int(i.value)
    print(sum)
    idWinner = sum % len(allPlayers)
    idWinner += 1
    print(idWinner)
    for i in allPlayers:
        if(i.id == str(idWinner)):
            return i

print("Deseja entrar no jogo? (Y / N)")
msg = str(input())

if (msg == 'Y' or msg == 'y'):
    udp.sendto(msg.encode(), dest)

    while True:
        
        serverMsg, serverAddress = udp.recvfrom(2048)
        msg = serverMsg.decode()
        print(msg)
        PEERS = getPeers(msg)
        info = msg.split('\n')

        if(MY_IP == None):
            MY_IP = getIP(info[len(info)-2])
        
        if (len(info) - 2 == PEERS):
            print("Link Start")

            udp.close()

            allPlayers = getPlayers(info, PEERS)
            ips = getListIP()

            threadRcv = threading.Thread(target=receiveValue)
            threadRcv.start()

            n = choseNumber()
            setValueOnIP(MY_IP, n)

            threadSend = threading.Thread(target=sendValue, args=[n, ips])
            threadSend.start()

            while threadRcv.isAlive():
                print("Recebendo os valores dos outros jogadores ...")
                time.sleep(20)                    
            # A partir deste ponto o usuário já pode definir o vencedor

            while threadSend.isAlive():
                print("Aguardando os outros jogadores receberem o seu valor ...")
                time.sleep(20)
            # A partir deste ponto todos os outros jogadores já sabem o valor escolhido por este usuário

            break
            
    win = getWinner()
    print("ID: " + win.id + " IP: " + win.ip)

input()
