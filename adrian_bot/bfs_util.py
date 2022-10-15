


from queue import Queue
from re import sub
from bot_utilities import TileType
from game_state import GameInstance

moves = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]
moves_diag = [
    (1, 1)
    (-1, 1)
    (-1, -1)
    (1, -1)
]

def add_pos(pos_a, pos_b):
    return int(pos_a[0]+pos_b[0]), int(pos_a[1]+pos_b[1])

def sub_pos(pos_a, pos_b):
    return int(pos_a[0]-pos_b[0]), int(pos_a[1]-pos_b[1])

def get_target_exploring(game_instance: GameInstance, target_pos=None):
    pathtrace_direction = {game_instance.player_pos: (0,0)} # from coordinate to coordinate delta
    search_queue = Queue()
    search_queue.put(game_instance.player_pos)
    
    while not search_queue.empty() or target_found:
        cur = search_queue.get(0)
        valid_moves = []
        target_found = None
        for move in moves:
            new_pos = add_pos(cur, move)
            if not new_pos in pathtrace_direction:
                pathtrace_direction[new_pos] = move
                search_queue.put(new_pos)
                if game_instance.get_tile_at(new_pos) == TileType.UNEXPLORED or new_pos == target_pos:
                    target_found = new_pos
                    break
                valid_moves.append(True)
            else:
                valid_moves.append(False)
        for i in range(4):
            if not (valid_moves[i] and valid_moves[(i+1) % 4]):
                continue
            move = moves_diag[i]
            new_pos = add_pos(cur, move)
            if not new_pos in pathtrace_direction:
                pathtrace_direction[new_pos] = move
                search_queue.put(new_pos)
                if game_instance.get_tile_at(new_pos) == TileType.UNEXPLORED or new_pos == target_pos:
                    target_found = new_pos
                    break
    return target_found, pathtrace_direction


def get_move_position_from_trace(target_pos, trace):
    cur_pos = target_pos
    last_direction = None
    last_straight_endpoint = cur_pos
    while trace[cur_pos] != (0, 0):
        if last_direction != trace[cur_pos]:
            last_straight_endpoint = cur_pos
        last_direction = trace[cur_pos]
        cur_pos = sub_pos(cur_pos, last_direction)
    return cur_pos

# def get_target_key(game_instance: GameInstance):

