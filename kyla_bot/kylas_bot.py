import socket
import time
import random
import bot_utilities as bot
 

msgFromClient       = "requestjoin:KylaBot"
name = "KylaBot"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 11000)

bufferSize          = 1024

directions = ["n","s","e","w","nw","sw","ne","se"]


# Create a UDP socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

 
moveInterval = 0.1
timeSinceMove = time.time()


def SendMessage(requestmovemessage):
    bytesToSend = str.encode(requestmovemessage)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)



while True:

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
    ##uncomment to see message format from server
    # print(msgFromServer)

    msgFromServerParsed = bot.parse_server_message(msgFromServer)

    if msgFromServerParsed[0] == bot.MsgType.P_JOINED:
        pos = msgFromServer.split(":")[1]
        posSplit = pos.split(",")
        posx = float(posSplit[2])
        posy = float(posSplit[3])

    if msgFromServerParsed[0] == bot.MsgType.P_UPDATE:
        pos = msgFromServer.split(":")[1]
        posSplit = pos.split(",")
        posx = float(posSplit[0])
        posy = float(posSplit[1])

    if msgFromServerParsed[0] == bot.MsgType.NEAR_PLAYER:
        enemyClass, enemyName, enemyX, enemyY = msgFromServerParsed[1]
        enemyDistance = bot.getEnemyDistance(enemyX, enemyY, posx, posy)
        enemyDirection = bot.getEnemyDirection(enemyX, enemyY, posx, posy)

        if enemyDirection in ["n", "s", "w", "e"] and enemyDistance < 1000:
            print("firing on the cross")
            bot.faceDirection(enemyDirection, UDPClientSocket, serverAddressPort)
            bot.fire(UDPClientSocket, serverAddressPort)
        
        elif enemyDirection in ["nw", "ne", "sw", "se"] and enemyDistance < 32:
            print("firing on the diagonal")
            bot.faceDirection(enemyDirection, UDPClientSocket, serverAddressPort)
            bot.fire(UDPClientSocket, serverAddressPort)

    now = time.time()
    if (now - timeSinceMove) > moveInterval:
        randomX = random.randrange(-50,50)
        randomY = random.randrange(-50,50)
        posx += randomX
        posy += randomY

        timeSinceMove = time.time()
        requestmovemessage = "moveto:" + str(posx)  + "," + str(posy)
        SendMessage(requestmovemessage)
        print(requestmovemessage)