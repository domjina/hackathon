import socket
import math
import bot_utilities as bu
from game_state import GameInstance

"""
@parmaters:
    UDP_IP - The IP address
    UDP_PORT - The port number
"""
def connect(connection: tuple, game: GameInstance, displayname) -> object:                       #This function creates a connection between the client and the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    displayname_decoded = displayname.decode("ascii")
    MESSAGE = b"requestjoin:"+displayname
    sock.sendto(MESSAGE, connection)
    joined = False
    while joined == False:
        msgFromServer_decoded = sock.recvfrom(1024)[0].decode("ascii")
        msgFromServerParsed = bu.parse_server_message(msgFromServer_decoded)
        if msgFromServerParsed[0] == bu.MsgType.P_JOINED:
            game.players[msgFromServerParsed[1][0]] = (msgFromServerParsed[1][1], msgFromServerParsed[1][2])
            if msgFromServerParsed[1][1] == displayname_decoded:
                game.player_color = msgFromServerParsed[1][0]
                game.player_pos = msgFromServerParsed[1][2]
                joined = True
        # # data, addr = sock.recvfrom(1024)
        # if b"JH02" in data:
        #     joined = True
    print("Connected to:",connection[0] + ", On port:", connection[1], "as", game.player_color.name)
    # data = str(data).split(",")
    # startX=math.floor(float(data[2].replace("'","")))
    # startY=math.floor(float(data[3].replace("'","")))
    return sock, connection #, startX, startY

"""
@parameters:
    posX - The x position to move to
    posY - The y position to move to
"""
def move(curPos: tuple, posX: str, posY: str, connection: object, connected_on: tuple) -> None:   #Takes the players current coordinates and how much to offset them by
    message = "moveto:{newX},{newY}".format(newX = posX, newY = posY)
    # print(message)
    connection.sendto(str.encode(str(message)), connected_on)
    # has_moved = False
    # while has_moved == False:
    #     msgFromServer_decoded = connection.recvfrom(1024)[0].decode("ascii")
    #     msgFromServerParsed = bu.parse_server_message(msgFromServer_decoded)
    #     if msgFromServerParsed[0] == bu.MsgType.P_UPDATE:
    #         if curPos[0] not in msgFromServerParsed[1]:
    #             has_moved = True
    # print("Player has moved")


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