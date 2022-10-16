import doms_bot_utilities as dbu
import bot_utilities as bu
import bot_movements as bot
from game_state import *
from bfs_util import *
import sys

mappedWalls = [[]]
mappedFloor = [[]]

stuffOfInterest = {"exit" : "", "food":"", "ammo":""}

nearby_floors = []

# player_class = "warrior"

game = GameInstance()
# sock, connection, curX, curY = dbu.connect(("127.0.0.1", 11000), game, b"JH02")
# print(sys.argv)
sock, connection = dbu.connect(("127.0.0.1", 11000), game, b"JH02" if len(sys.argv) < 2 else sys.argv[1].encode())

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
    for _ in range(2):
        msgFromServer_decoded = sock.recvfrom(1024)[0].decode("ascii")
        msgFromServerParsed = bu.parse_server_message(msgFromServer_decoded)
        if msgFromServerParsed[0] == bu.MsgType.NEAR_ITEM:
            for element in msgFromServerParsed[1]:
                if element[0] == bu.ItemType.KEY:
                    if game.player_color == element[2]:
                        game.key_pos = element[1]
                        # dbu.move((curX, curY), element[1][0]-curX, element[1][1]-curY, sock, connection)
                        # curX += element[1][0] - curX
                        # curY += element[1][1] - curY
                        # break
                elif element[0] == bu.ItemType.AMMO:
                    game.ammos.add(element[1])
                elif element[0] == bu.ItemType.TREASURE:
                    game.treasures.add(element[1])
                elif element[0] == bu.ItemType.FOOD:
                    game.foods.add(element[1])
        elif msgFromServerParsed[0] == bu.MsgType.NEAR_PLAYER:
            posx, posy = game.player_pos
            enemyClass, enemyName, (pos) = msgFromServerParsed[1]
            enemyX, enemyY = pos
            enemyDistance = bot.getEnemyDistance(enemyX, enemyY, posx, posy)
            enemyDirection = bot.getEnemyDirection(enemyX, enemyY, posx, posy)
            # if enemyDirection in ["n", "s", "w", "e"] and enemyDistance < 400:
            #     bot.faceDirection(enemyDirection, sock, connection)
            #     bot.fire(sock, connection)
            #     print("FIREEEEEEEEEEEEEEE")
        
            # elif enemyDirection in ["nw", "ne", "sw", "se"] and enemyDistance < 200:
            #     bot.faceDirection(enemyDirection, sock, connection)
            #     bot.fire(sock, connection)
            #     print("FIREEEEEEEEEEEEEEE")
        
            # else:
            #     if game.ammos != 0:
            #         bot.moveDirection(enemyDirection, sock, connection)
            #         bot.fire(sock, connection)
            if game.playerammo != 0:
                bot.moveDirection(enemyDirection, sock, connection)
                bot.fire(sock, connection)
            #if math.sqrt(ms)s
        elif msgFromServerParsed[0] == bu.MsgType.NEAR_WALLS:
            for pos in msgFromServerParsed[1]:
                game.explore_wall(*pos)

        # elif msgFromServerParsed[0] == bu.MsgType.P_JOINED:

        elif msgFromServerParsed[0] == bu.MsgType.NEAR_FLOORS:
            for pos in msgFromServerParsed[1]:
                game.explore_floor(*pos)
                game.ammos.discard(pos)
                game.treasures.discard(pos)
                game.foods.discard(pos)
        elif msgFromServerParsed[0] == bu.MsgType.P_UPDATE:
            game.player_pos = msgFromServerParsed[1][0]
            game.explore_floor(*game.player_pos)
            game.health = msgFromServerParsed[1][1]
            game.playerammo = msgFromServerParsed[1][2]
            game.has_key = msgFromServerParsed[1][3]

            if game.has_key:
                game.nav_target = game.exit
            
            # print("floors: ", msgFromServerParsed[1])
            # bfspath_data = get_target_exploring(game, game.nav_target)
            # next_move = get_move_position_from_trace(*bfspath_data)
            # print("from: ", game.player_pos)
            # print("next move: ", next_move)
            # dbu.move(game.player_pos, *next_move, sock, connection)
        elif msgFromServerParsed[0] == bu.MsgType.EXIT:
            game.exit = msgFromServerParsed[1][0]
            print("EXIT = ", game.exit)
        else:
            print(msgFromServerParsed)

    bfspath_data = None, None
    # strategy planning & response
    if game.foods or game.treasures or game.ammos:
        game.nav_target = None
        bfspath_data = get_target_exploring(game, game.nav_target, game.foods.union(game.treasures).union(game.ammos))
    # elif game.foods:
    #     game.nav_target = None
    #     bfspath_data = get_target_exploring(game, game.nav_target, game.foods)
    # elif game.treasures:
    #     game.nav_target = None
    #     bfspath_data = get_target_exploring(game, game.nav_target, game.treasures)
    # elif game.ammos:
    #     game.nav_target = None
    #     bfspath_data = get_target_exploring(game, game.nav_target, game.ammos)
    # else:
    if not bfspath_data[0]:
        game.nav_target = game.exit
        if not game.has_key:
            game.nav_target = game.key_pos
        bfspath_data = get_target_exploring(game, game.nav_target)
    if not bfspath_data[0]:
        print("ERROR - BFS path not found")
    else:
        next_move = get_move_position_from_trace(*bfspath_data)
        dbu.move(game.player_pos, *next_move, sock, connection)


    # bug: hardcoded player color
        

