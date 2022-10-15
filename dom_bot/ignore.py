import socket
import random

places_seen = [] #empty list
UDP_IP = "127.0.0.1"
UDP_PORT = 11000
name = "JH02"
MESSAGE = b"requestjoin:JH02"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
possible_moves = [1,-1,1,-1]

#This is responsible for connecting to the server and calling move
def main():
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    try:
        have_joined()
        print("Has joined")
    except socket.error as e:
        print("Could not join:",e)

    move()

def have_joined():
    joined = False
    while joined == False:
        data, addr = sock.recvfrom(1024)
        if b"JH02" in data:
            joined = True


#responsible for moving the player
def move():
    for i in range(4): #Just trying to move 4 random places
        move_to = possible_moves[random.randint(0,3)]
        move = "moveto:{xPos},{yPos}".format(xPos=move_to, yPos=move_to)
        sock.sendto(bytes(move, encoding="UTF-8"), (UDP_IP, UDP_PORT)) #Send the coordinates to the server
        player_has_moved(move) #Check if player has moved
    print("Done")

def player_has_moved(moving_to):
    has_moved = False
    for i in range(100):
        if has_moved == False:
            data, addr = sock.recvfrom(1024)
            moved = "{message}".format(message = moving_to)
            if bytes(moved, encoding="UTF-8") in data:
                has_moved = True
                print("Has moved")
    if has_moved == False:
        print("Has not moved")

if __name__ == "__main__":
    main()