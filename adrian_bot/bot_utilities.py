from ctypes.wintypes import MSG
from enum import Enum, auto
from re import A


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

player_class_to_color = {
    "warrior": PlayerColor.RED,
    "elf": PlayerColor.GREEN,
    "wizard": PlayerColor.YELLOW,
    "valkyrie": PlayerColor.BLUE,
}

map_item_name = {
    "key": ItemType.KEY,
    "ammo": ItemType.AMMO,
    "food": ItemType.FOOD,
    "treasure": ItemType.TREASURE,
    "player": ItemType.PLAYER,
    "exit": ItemType.EXIT,
}

def parse_server_message(msg, debug=False):
    args = msg.strip(',').split(",")
    msg_type, args[0] = args[0].split(":")
    args_parsed = []

    if msg_type == "playerjoined":
        msg_type = MsgType.P_JOINED
        args_parsed = [args[0], args[1], (float(args[2]), float(args[3]))]
    elif msg_type == "playerupdate":
        msg_type = MsgType.P_UPDATE
        args_parsed = [(float(args[0]), float(args[1])), float(args[2]), float(args[3]), args[4] == "True"]
    elif msg_type in ["nearbywalls", "nearbyfloors"]:
        msg_type = MsgType.NEAR_FLOORS if msg_type == "nearbyfloors" else MsgType.NEAR_WALLS
        args_parsed = [(float(args[0]), float(args[1])), (float(args[2]), float(args[3]))]
    elif msg_type == "nearbyitem":
        msg_type = MsgType.NEAR_ITEM
        for i in range(0, len(args), 3):
            if args[i] not in map_item_name:
                print(f"ITEM TYPE '{ args[i] }' IS UNDEFINED")
                continue
            args_parsed.append((map_item_name[args[i]], (float(args[i+1]), float(args[i+2]))))
    elif msg_type == "nearbyplayer":
        msg_type = MsgType.NEAR_PLAYER
        args_parsed = [args[0], (float(args[1]), float(args[2]))]
    elif msg_type == "exit":
        msg_type = MsgType.EXIT
        args_parsed = [(float(args[0]), float(args[1]))]
    else:
        print(f"!!!   MESSAGE TYPE '{ msg_type }' IS UNDEFINED   !!!")
    # if debug: print((msg_type, args_parsed))
    return msg_type, args_parsed



def make_move(player_pos, player_ori, target_pos):
    global sck




# print(parse_server_message("abc:1,3.2,False,6", True))
