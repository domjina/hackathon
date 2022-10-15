


from queue import Queue
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

def get_target_exploring(game_instance: GameInstance):
    pathtrace_direction = {} # from coordinate to coordinate delta 
    search_queue = Queue()
    search_queue.put(game_instance.player_pos)
    
    while search_queue:
        cur = search_queue.get(0)
        valid_moves = []
        for move in moves:
            new_pos = add_pos(cur, move)
            if not new_pos in pathtrace_direction:
                pathtrace_direction[new_pos] = move
                search_queue.put(new_pos)
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
                if 
        
    return 



def get_target_key(game_instance: GameInstance):

