


from queue import Queue
from bot_utilities import TileType
from game_state import GameInstance

gridsize = 8
moves = [
    (1*gridsize, 0),
    (0, 1*gridsize),
    (-1*gridsize, 0),
    (0, -1*gridsize),
]
moves_diag = [
    (1*gridsize, 1*gridsize),
    (-1*gridsize, 1*gridsize),
    (-1*gridsize, -1*gridsize),
    (1*gridsize, -1*gridsize),
]

def normalize_pos_grid(pos):
    return (pos[0]//gridsize)*gridsize, (pos[1]//gridsize)*gridsize

def add_pos(pos_a, pos_b):
    return int(pos_a[0]+pos_b[0]), int(pos_a[1]+pos_b[1])

def sub_pos(pos_a, pos_b):
    return int(pos_a[0]-pos_b[0]), int(pos_a[1]-pos_b[1])

def get_target_exploring(game_instance: GameInstance, target_pos=None, target_type=set()):
    player_pos = normalize_pos_grid(add_pos(game_instance.player_pos, (4,4)))
    # player_pos = normalize_pos_grid(game_instance.player_pos)
    pathtrace_direction = {player_pos: (0,0)} # from coordinate to coordinate delta
    search_queue = Queue()
    search_queue.put(player_pos)
    target_found = None
    
    while not search_queue.empty() and not target_found:
        cur = search_queue.get(0)
        valid_moves = []
        for move in moves:
            new_pos = add_pos(cur, move)
            # if not (new_pos in pathtrace_direction and game_instance.get_tile_at(*new_pos) != TileType.WALL):
            if not new_pos in pathtrace_direction and not game_instance.get_tile_at(*new_pos) == TileType.WALL:

                pathtrace_direction[new_pos] = move
                search_queue.put(new_pos)
                if ((game_instance.get_tile_at(*new_pos) == TileType.UNEXPLORED or new_pos in target_type) and not target_pos) or new_pos == target_pos: # bug found!
                    target_found = new_pos
                    break
                valid_moves.append(True)
            else:
                valid_moves.append(False)
        if not target_found:
            for i in range(4):
                if not (valid_moves[i] and valid_moves[(i+1) % 4]):
                    continue
                move = moves_diag[i]
                new_pos = add_pos(cur, move)
                if not new_pos in pathtrace_direction and not game_instance.get_tile_at(*new_pos) == TileType.WALL:
                    pathtrace_direction[new_pos] = move
                    search_queue.put(new_pos)
                    if ((game_instance.get_tile_at(*new_pos) == TileType.UNEXPLORED or new_pos in target_type) and not target_pos) or new_pos == target_pos: # bug found!
                    # if game_instance.get_tile_at(*new_pos) == TileType.UNEXPLORED or new_pos == target_pos:
                        target_found = new_pos
                        break
    return target_found, pathtrace_direction


def get_move_position_from_trace(target_pos, trace):
    cur_pos = target_pos
    last_direction = None
    last_straight_endpoint = cur_pos
    
    while trace[cur_pos] != (0, 0):
        # print(cur_pos, trace[cur_pos])
        if last_direction != trace[cur_pos]:
            last_straight_endpoint = cur_pos
        last_direction = trace[cur_pos]
        cur_pos = sub_pos(cur_pos, last_direction)
    return last_straight_endpoint

# def get_target_key(game_instance: GameInstance):

