import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 11000
name = "JH02"
MESSAGE = b"requestjoin:JH02"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main():
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    try:
        haveJoined()
    except socket.error as e:
        print("Could not join:",e)


    print("done")

def haveJoined():
    joined = False
    while joined == False:
        data, addr = sock.recvfrom(1024)
        if b"playerjoined:warrior,JH02" in data:
            joined = True

if __name__ == "__main__":
    main()