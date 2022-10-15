from operator import ge
import doms_bot_utilities as dbu
import bot_utilities as bu
import math
from game_state import *
from bfs_util import *

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

game = GameInstance()

while True:
    msgFromServer_decoded = sock.recvfrom(1024)[0].decode("ascii")
    msgFromServerParsed = bu.parse_server_message(msgFromServer_decoded)
    if msgFromServerParsed[0] == bu.MsgType.NEAR_ITEM:
        for element in msgFromServerParsed[1]:
            if element[0] == bu.ItemType.KEY:
                if bu.playerclass_to_playercolor[player_class] == element[2]:
                    game.nav_target = element[1][0], element[1][1]
                    # dbu.move((curX, curY), element[1][0]-curX, element[1][1]-curY, sock, connection)
                    # curX += element[1][0] - curX
                    # curY += element[1][1] - curY
                    # break
            if element[0] == bu.ItemType.EXIT:
                game.exit = element[1]
                print("EXIT item = ", game.exit)
    elif msgFromServerParsed[0] == bu.MsgType.NEAR_PLAYER:
        if math.sqrt((curX - msgFromServerParsed[1][2][0]) + (curY - msgFromServerParsed[1][2][1])):
            print("FIREEEEEEEEEEEEEEE")
        #if math.sqrt(ms)s
    elif msgFromServerParsed[0] == bu.MsgType.NEAR_WALLS:
        for pos in msgFromServerParsed[1]:
            game.explore_wall(*pos)

    elif msgFromServerParsed[0] == bu.MsgType.NEAR_FLOORS:
        for pos in msgFromServerParsed[1]:
            game.explore_floor(*pos)

        # print("floors: ", msgFromServerParsed[1])
        bfspath_data = get_target_exploring(game, game.nav_target)
        next_move = get_move_position_from_trace(*bfspath_data)
        # print("from: ", game.player_pos)
        # print("next move: ", next_move)
        dbu.move(game.player_pos, *next_move, sock, connection)
    elif msgFromServerParsed[0] == bu.MsgType.P_UPDATE:
        game.player_pos = msgFromServerParsed[1][0]
        game.explore_floor(*game.player_pos)
        game.health = msgFromServerParsed[1][1]
        game.ammo = msgFromServerParsed[1][2]
        game.has_key = msgFromServerParsed[1][3]

        if game.has_key:
            game.nav_target = game.exit
        
    elif msgFromServerParsed[0] == bu.MsgType.EXIT:
        game.exit = msgFromServerParsed[1][0]
        print("EXIT = ", game.exit)
    else:
        print(msgFromServerParsed)
    
    
        

