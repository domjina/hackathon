import doms_bot_utilities as dbu
import bot_utilities as bu
import math

mappedWalls = [[]]
mappedFloor = [[]]

stuffOfInterest = {"exit" : "", "food":"", "ammo":""}

nearby_floors = []

player_class = "warrior"

sock, connection, curX, curY = dbu.connect(("127.0.0.1", 11000))

#while True:
#    visited_but_unprocessed = []
#    visited_but_unprocessed.append(nearby_floors)
#    while visited_but_unprocessed is not None:
        #moveToVisitedButUnprocessed.POP()
        #new_tiles = []
        #for (coords in nearby_floors):
            #if coords not in visited_but_unprocessed:
                #new_tiles.append(coords)
        #for coords in new_tiles:
            #if coords not in mappedFloor
                #mappedFloors.append(list(coords))
                #visited_but_unprocessed.append(coords)
        #pass


while True:
    msgFromServer_decoded = sock.recvfrom(1024)[0].decode("ascii")
    msgFromServerParsed = bu.parse_server_message(msgFromServer_decoded)
    if msgFromServerParsed[0] == bu.MsgType.NEAR_ITEM:
        for element in msgFromServerParsed[1]:
            if element[0] == bu.ItemType.KEY :
                if bu.playerclass_to_playercolor[player_class] == element[2]:
                    dbu.move((curX, curY), element[1][0]-curX, element[1][1]-curY, sock, connection)
                    curX += element[1][0] - curX
                    curY += element[1][1] - curY
                    break

    elif msgFromServerParsed[0] == bu.MsgType.NEAR_PLAYER:
        if math.sqrt((curX - msgFromServerParsed[1][2][0]) + (curY - msgFromServerParsed[1][2][1])):
            print("FIREEEEEEEEEEEEEEE")
        #if math.sqrt(ms)s