from bot_utilities import *

class GameInstance:

    def __init__(self) -> None:
        self.game_floorplan = {}
        self.player_pos = (0, 0)
        self.player_color = None
        self.nav_target = None
        self.has_key = False
        self.key_pos = None
        self.health = 100
        self.playerammo = 10
        self.last_position = (0,0)
        self.exit = None
        self.players = {}
        self.foods = set()
        self.ammos = set()
        self.treasures = set()

    def explore_floor(self, x, y):
        self.game_floorplan[(int(x), int(y))] = TileType.FLOOR

    def explore_wall(self, x, y):
        self.game_floorplan[(int(x), int(y))] = TileType.WALL

    def set_player_position(self, x, y):
        self.player_pos = (x, y)

    def get_tile_at(self, x, y):
        # print(x, y, self.game_floorplan.get((int(x), int(y)), TileType.UNEXPLORED))
        return self.game_floorplan.get((int(x), int(y)), TileType.UNEXPLORED)
    
