import socket
import threading, time
from Player import inGamePlayer

HOST = '172.22.75.183'
PORT = 5000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

# Alterar estes valores para padronizar (para o caso de vários jogadores)
PORT_RCV_VALUE = 6000
PORT_SND_VALUE = 6000
KNOWN_VALUES = 1
MY_IP = None
allPlayers = []

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

def sendValue(valor, ips):
    udpSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = str(valor)
    for i in ips:
        attempts = 0
        successful = False
        while (attempts < 6 and not successful):
            if (i != MY_IP): # Evita que envie para si mesmo
                destPlayer = (i, PORT_SND_VALUE)
                print("Enviando " + msg + " para " + i + " na porta " + str(PORT_SND_VALUE))
                udpSend.sendto(msg.encode('utf-8'), destPlayer)
                print("Enviado")
                # Aguarda ACK
                serverMsg, serverAddress = udpSend.recvfrom(2048)
                if (serverMsg.decode() == "OK"):
                    print("Sucesso")
                    successful = True
                else:
                    time.sleep(5)
                    attempts += 1
            else:
                successful = True
        if not successful:
            # Caso o IP não responde depois de 6 tentativas (30 segundos) será considerado como desconectado e removido da partida
            removePlayerByIP(i)
    udpSend.close()

def receiveValue():
    global KNOWN_VALUES
    while (KNOWN_VALUES < PEERS): # Caso não conheça o valor de todos os jogadores, aguarda recebê-los
        orig = (MY_IP, PORT_RCV_VALUE)
        udpRcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpRcv.bind(orig)
        print("Esperando: " + MY_IP + ", " + str(PORT_RCV_VALUE))
        # Espera receber um valor
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
        # Encerra este socket para poder esperar o próximo valor
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

            thread2 = threading.Thread(target=receiveValue)
            thread2.start()

            n = choseNumber()
            setValueOnIP(MY_IP, n)

            thread1 = threading.Thread(target=sendValue, args=[n, ips])
            thread1.start()
            

            # Envia o seu valor aos outros jogadores
            # sendValue(n, ips)
            # Recebe os valores dos outros jogadores
            # receiveValue()

            while thread2.isAlive():
                print("Recebendo os valores dos outros jogadores ...")
                time.sleep(5)
            # A partir deste ponto o usuário já pode definir o vencedor

            while thread1.isAlive():
                print("Aguardando os outros jogadores receberem o seu valor ...")
                time.sleep(5)
            # A partir deste ponto todos os outros jogadores já sabem o valor escolhido por este usuário

            break
            
    win = getWinner()
    print("ID: " + win.id + " IP: " + win.ip)

input()
