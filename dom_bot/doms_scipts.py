import socket

"""
@parmaters:
    UDP_IP - The IP address
    UDP_PORT - The port number
"""
def connect(connection: tuple) -> object:                       #This function creates a connection between the client and the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = b"requestjoin:JH02"
    sock.sendto(MESSAGE, connection)
    joined = False
    while joined == False:
        data, addr = sock.recvfrom(1024)
        if b"JH02" in data:
            joined = True
    print("Connected to:",connection[0] + ", On port:", connection[1])
    return sock

"""
@parameters:
    posX - The x position to move to
    posY - The y position to move to
"""
def move(curX: str, curY: str, posX: str, posY: str, connection: object) -> None:   #Takes the players current coordinates and how much to offset them by
    message = "moveto:",(curX+posX),",",(curY+posY)
    connection.sendto(message)
    has_moved = False
    while has_moved == False:
        data, addr = connection.recvfrom(1024)
        if str.encode(str(curX+posX)) in data:
            has_moved = True
    print("Player has moved to position:", (curX + posX))


"""
@parameters:
    connection - The connection used by the client
"""
def getPlayerPosition(connection: object) -> tuple:             #Takes a connection and waits to recieve the player update message
    recievedUpdate = False
    while recievedUpdate == False:
        data, addr = connection.recvfrom(1024)
        if b"playerupdate" in data:
            recieved = data.decode().split(",")
            posX = recieved[1]
            posY = recieved[2]
            return (posX, posY)