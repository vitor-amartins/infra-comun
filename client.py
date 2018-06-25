import socket
HOST = '172.22.79.112'
PORT = 5000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
print("Deseja entrar no jogo? (Y / N)")
msg = input()

if (msg == 'Y'):
    udp.sendto(msg.encode(), dest)

while True:
    serverMsg, serverAddress = udp.recvfrom(2048)
    print(serverMsg.decode())

input()
udp.close()