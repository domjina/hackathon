def move(curPos: tuple, posX: str, posY: str, connection: object, connected_on: tuple) -> None:   #Takes the players current coordinates and how much to offset them by
    newX = curPos[0] + posX
    newY = curPos[1] + posY
    message = f"moveto:{newX},{newY}"
    print(message)
    connection.sendto(str.encode(message), connected_on)

def moveDirection(direction, connection, connected_on):
    message = f"movedirection:{direction}"
    connection.sendto(str.encode(message), connected_on)

def fire(connection, connected_on):
    message = "fire:"
    connection.sendto(str.encode(message), connected_on)

def getEnemyDistance(enemyX, enemyY, posx, posy):
    return (enemyX - posx)**2 + (enemyY - posy)**2

def getEnemyDirection(enemyX, enemyY, posx, posy):
    default_direction = "nw"
    direction = default_direction

    if abs(enemyX - posx) < 5:
        if (enemyY < posy):
            direction = "n"
        else:
            direction = "s"
    elif abs(enemyY - posy) < 5:
        if (enemyX > posx):
            direction = "e"
        else:
            direction = "w"
    elif (enemyX > posx):
        if (enemyY < posy):
            direction = "ne"
        else:
            direction = "se"
    elif (enemyX < posx):
        if (enemyY > posy):
            direction = "sw"
    else:
        direction = "nw"
        
    return direction

def faceDirection(direction, connection, connected_on):
    directionFaceMessage = "facedirection:" + direction
    connection.sendto(str.encode(directionFaceMessage), connected_on)
    print(directionFaceMessage)