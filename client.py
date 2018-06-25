import socket

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

def getIPs(info, peers):
    ip = []
    j = 1
    while (j <= peers):
        i = info[j].find("IP: ") + len("IP: ")
        str1 = ''
        while(info[j][i] != ' '):
            str1 += info[j][i]
            i += 1
        print(str1)
        j += 1
        ip.append(str1)
    return ip

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
    
    if (len(info) - 2 == PEERS):
        print("Link Start")
        ips = getIPs(info, PEERS)
        n = choseNumber()
        print(n)
        # Enviar a todos os IP's

input()
udp.close()