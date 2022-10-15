from enum import Enum, auto
import math


class MsgType(Enum):
    P_JOINED = auto()
    P_UPDATE = auto()
    NEAR_PLAYER = auto()
    NEAR_ITEM = auto()
    NEAR_WALLS = auto()
    NEAR_FLOORS = auto()
    EXIT = auto()

class ItemType(Enum):
    # WALL = auto()
    # FLOOR = auto()
    KEY = auto()
    AMMO = auto()
    FOOD = auto()
    TREASURE = auto()
    PLAYER = auto()
    EXIT = auto()

class PlayerColor(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()

playerclass_to_playercolor = {
    "warrior": PlayerColor.RED,
    "elf": PlayerColor.GREEN,
    "wizard": PlayerColor.YELLOW,
    "valkyrie": PlayerColor.BLUE,
}

color_to_playercolor = {
    "red": PlayerColor.RED,
    "green": PlayerColor.GREEN,
    "yellow": PlayerColor.YELLOW,
    "blue": PlayerColor.BLUE,
}

itemname_to_itemtype = {
    "redkey": ItemType.KEY,
    "greenkey": ItemType.KEY,
    "yellowkey": ItemType.KEY,
    "bluekey": ItemType.KEY,
    "ammo": ItemType.AMMO,
    "food": ItemType.FOOD,
    "treasure": ItemType.TREASURE,
    "player": ItemType.PLAYER,
    "exit": ItemType.EXIT,
}


# Format of output:
    # playerjoined: PlayerColor(Enum),  display_name,   (posX,posY)
    # playerupdate: (posX,posY),    health,     ammo,   hasKey
    # nearbywalls:  (posX,posY), (posX,posY), (posX,posY), .... (posX,posY pairs will repeat for every nearby wall segment)
    # nearbyfloors: (posX,posY), (posX,posY), (posX,posY), .... (posX,posY pairs will repeat for every nearby floor segment)
    # nearbyitem:   ( ItemType(Enum), (posX,posY), ?PlayerColor(Enum) ),    ....
    # nearbyplayer: PlayerColor(Enum),  (posX,posY)
    # exit:         (posX,posY)
def parse_server_message(msg, debug=False):
    args = msg.strip(',').split(",")
    msg_type, args[0] = args[0].split(":")
    args_parsed = []

    if msg_type == "playerjoined":
        msg_type = MsgType.P_JOINED
        if args[0] not in playerclass_to_playercolor:
            print(f"!!!   PLAYER CLASS '{ args[0] }' IS UNDEFINED   !!!")
        else:
            args_parsed = [playerclass_to_playercolor[args[0]], args[1], (float(args[2]), float(args[3]))]
    elif msg_type == "playerupdate":
        msg_type = MsgType.P_UPDATE
        args_parsed = [(float(args[0]), float(args[1])), float(args[2]), float(args[3]), args[4] == "True"]
    elif msg_type in ["nearbywalls", "nearbyfloors"]:
        msg_type = MsgType.NEAR_FLOORS if msg_type == "nearbyfloors" else MsgType.NEAR_WALLS
        args_parsed = [(float(args[0]), float(args[1])), (float(args[2]), float(args[3]))]
    elif msg_type == "nearbyitem":
        msg_type = MsgType.NEAR_ITEM
        for i in range(0, len(args), 3):
            if args[i] not in itemname_to_itemtype:
                print(f"!!!   ITEM TYPE '{ args[i] }' IS UNDEFINED   !!!")
                continue
            itype = itemname_to_itemtype[args[i]]
            icolor = None
            if itype == ItemType.KEY:
                icolor = color_to_playercolor[args[i][:-3]]
            args_parsed.append((itype, (float(args[i+1]), float(args[i+2])), icolor))
    elif msg_type == "nearbyplayer":
        msg_type = MsgType.NEAR_PLAYER
        if args[0] not in playerclass_to_playercolor:
            print(f"!!!   PLAYER CLASS '{ args[0] }' IS UNDEFINED   !!!")
        else:
            args_parsed = [playerclass_to_playercolor[args[0]], args[1], (float(args[2]), float(args[3]))]
    elif msg_type == "exit":
        msg_type = MsgType.EXIT
        args_parsed = [(float(args[0]), float(args[1]))]
    else:
        print(f"!!!   MESSAGE TYPE '{ msg_type }' IS UNDEFINED   !!!")
    # if debug: print((msg_type, args_parsed))
    return msg_type, args_parsed



def make_move(player_pos, player_ori, target_pos):
    global sck

def move(curPos: tuple, posX: str, posY: str, connection: object, connected_on: tuple) -> None:   #Takes the players current coordinates and how much to offset them by
    newX = curPos[0] + posX
    newY = curPos[1] + posY
    message = f"moveto:{newX},{newY}"
    print(message)
    connection.sendto(str.encode(message), connected_on)
    has_moved = False
    while has_moved == False:
        msgFromServer_decoded = connection.recvfrom(1024)[0].decode("ascii")
        msgFromServerParsed = parse_server_message(msgFromServer_decoded)
        if msgFromServerParsed[0] == MsgType.P_UPDATE:
            if curPos[0] not in msgFromServerParsed[1]:
                has_moved = True
    print("Player has moved")

def fire(connection, connected_on):
    message = "fire:"
    print(message)
    connection.sendto(str.encode(message), connected_on)
    print("Fire!")

def getEnemyDistance(enemyX, enemyY, posx, posy):
    return (enemyX - posx)**2 + (enemyY-posy)**2

def getEnemyDirection(enemyX, enemyY, posx, posy):
    d = getEnemyDistance(enemyX, enemyY, posx, posy)
    alpha = math.asin((enemyX-posx)/d) * 180/math.pi
    if alpha < 0:
        alpha = alpha + 360
    
    if alpha < 22.5:
        direction = "n"
    elif alpha < 67.5:
        direction = "ne"
    elif alpha < 112.5:
        direction = "e"
    elif alpha < 157.5:
        direction = "se"
    elif alpha < 202.5:
        direction = "s"
    elif alpha < 247.5:
        direction = "sw"
    elif alpha < 292.5:
        direction = "w"
    elif alpha < 337.5:
        direction = "nw"

    return direction

def faceDirection(direction, connection, connected_on):
    directionFaceMessage = "facedirection:" + direction
    connection.sendto(str.encode(directionFaceMessage), connected_on)
    print(directionFaceMessage)



# print(parse_server_message("abc:1,3.2,False,6", True))
