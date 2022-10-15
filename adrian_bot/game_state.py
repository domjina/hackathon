from bot_utilities import *

class GameInstance:

    def __init__(self) -> None:
        self.game_floorplan = {}
        self.player_pos = (0, 0)
        self.nav_target = None
        self.has_key = False
        self.health = 100
        self.ammo = 10
        self.exit = None

    def explore_floor(self, x, y):
        self.game_floorplan[(int(x), int(y))] = TileType.FLOOR

    def explore_wall(self, x, y):
        self.game_floorplan[(int(x), int(y))] = TileType.WALL

    def set_player_position(self, x, y):
        self.player_pos = (x, y)

    def get_tile_at(self, x, y):
        # print(x, y, self.game_floorplan.get((int(x), int(y)), TileType.UNEXPLORED))
        return self.game_floorplan.get((int(x), int(y)), TileType.UNEXPLORED)
    
