import socket
import time
import random
import bot_utilities as bot
 

msgFromClient       = "requestjoin:KylaBot"
name = "KylaBot"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 11000)

bufferSize          = 1024

#bunch of timers and intervals for executing some sample commands
moveInterval = 0.1
timeSinceMove = time.time()

fireInterval = 5
timeSinceFire = time.time()

stopInterval = 30
timeSinceStop = time.time()

directionMoveInterval = 15
timeSinceDirectionMove = time.time()

directionFaceInterval = 9
timeSinceDirectionFace = time.time()

directions = ["n","s","e","w","nw","sw","ne","se"]


# Create a UDP socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

 



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
    
    if msgFromServerParsed[0] == bot.MsgType.NEAR_ITEM:
        for element in msgFromServerParsed[1]:
            if element[0] == bot.ItemType.KEY:
                bot.move((posx, posy), element[1][0]-posx, element[1][1]-posy, UDPClientSocket, serverAddressPort)
                print("Got the key!")
                posx += element[1][0] - posx
                posy += element[1][1] - posy
            elif element[0] == bot.ItemType.TREASURE:
                bot.move((posx, posy), element[1][0]-posx, element[1][1]-posy, UDPClientSocket, serverAddressPort)
                print("Got the treasure!")
                posx += element[1][0] - posx
                posy += element[1][1] - posy
    
    if msgFromServerParsed[0] == bot.MsgType.NEAR_PLAYER:
        enemyName, enemyX, enemyY = msgFromServerParsed[1].split(",")
        enemyDistance = bot.getEnemyDistance(enemyX, enemyY, posx, posy)
        if enemyDistance < 16:
            enemyDirection = bot.getEnemyDirection(enemyX, enemyY, posx, posy)
            bot.faceDirection(enemyDirection, UDPClientSocket, serverAddressPort)
            bot.fire(UDPClientSocket, serverAddressPort)
        # this would be a good place to make a hunter bot




    now = time.time()

    # #every few seconds, request to move to a random point nearby. No pathfinding, server will 
    # #attempt to move in straight line.
    if (now - timeSinceMove) > moveInterval:
        randomX = random.randrange(-50,50)
        randomY = random.randrange(-50,50)
        posx += randomX
        posy += randomY

        timeSinceMove = time.time()
        # requestmovemessage = "moveto:" + str(posx)  + "," + str(posy)
        # SendMessage(requestmovemessage)
        # print(requestmovemessage)
        bot.move((posx, posy), randomX, randomY, UDPClientSocket, serverAddressPort)

    # #let's fire
    # if (now - timeSinceFire) > fireInterval:
    #     timeSinceFire = time.time()
    #     fireMessage = "fire:"
    #     SendMessage(fireMessage)
    #     print(fireMessage)
       
        

    # if(now - timeSinceStop) > stopInterval:
    #     stopMessage = "stop:"
    #     SendMessage(stopMessage)
    #     timeSinceStop = time.time()
    #     print(stopMessage)


    # if(now - timeSinceDirectionMove) > directionMoveInterval:

    #     randomDirection = random.choice(directions)
    #     directionMoveMessage = "movedirection:" + randomDirection
    #     SendMessage(directionMoveMessage)
    #     timeSinceDirectionMove = time.time()
    #     print(directionMoveMessage)

    # if(now - timeSinceDirectionFace) > directionFaceInterval:

    #     randomDirection = random.choice(directions)
    #     directionFaceMessage = "facedirection:" + randomDirection
    #     SendMessage(directionFaceMessage)
    #     timeSinceDirectionFace = time.time()
    #     print(directionFaceMessage)