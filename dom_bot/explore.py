import doms_scipts as ds
import bot_utilities as bu
mappedWalls = [[]]
mappedFloor = [[]]

stuffOfInterest = {"exit" : "", "food":"", "ammo":""}

nearby_floors = []

s = ds.connect(("127.0.0.1", 11000))
print(ds.getPlayerPosition(s))

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