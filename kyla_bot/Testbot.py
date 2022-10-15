
import socket
import time
import random
 
#Merge conflict just for kyla

msgFromClient       = "requestjoin:mydisplayname"
name = "mydisplayname"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 11000)

bufferSize          = 1024

#bunch of timers and intervals for executing some sample commands
moveInterval = 10
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
    #print(msgFromServer)
    
    if "playerupdate" in msgFromServer:
        pos = msgFromServer.split(":")[1]
        posSplit = pos.split(",")
        posx = float(posSplit[0])
        posy = float(posSplit[1])


    now = time.time()

    #every few seconds, request to move to a random point nearby. No pathfinding, server will 
    #attempt to move in straight line.
    if (now - timeSinceMove) > moveInterval:
        randomX = random.randrange(-50,50)
        randomY = random.randrange(-50,50)
        posx += randomX
        posy += randomY

        timeSinceMove = time.time()
        requestmovemessage = "moveto:" + str(posx)  + "," + str(posy)
        SendMessage(requestmovemessage)
        print(requestmovemessage)

    #let's fire
    if (now - timeSinceFire) > fireInterval:
        timeSinceFire = time.time()
        fireMessage = "fire:"
        SendMessage(fireMessage)
        print(fireMessage)
       
        

    if(now - timeSinceStop) > stopInterval:
        stopMessage = "stop:"
        SendMessage(stopMessage)
        timeSinceStop = time.time()
        print(stopMessage)


    if(now - timeSinceDirectionMove) > directionMoveInterval:

        randomDirection = random.choice(directions)
        directionMoveMessage = "movedirection:" + randomDirection
        SendMessage(directionMoveMessage)
        timeSinceDirectionMove = time.time()
        print(directionMoveMessage)

    if(now - timeSinceDirectionFace) > directionFaceInterval:

        randomDirection = random.choice(directions)
        directionFaceMessage = "facedirection:" + randomDirection
        SendMessage(directionFaceMessage)
        timeSinceDirectionFace = time.time()
        print(directionFaceMessage)



