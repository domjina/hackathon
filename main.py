import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 11000
name = "JH02"
MESSAGE = b"requestjoin:JH02"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main():
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    print("Done")

if __name__ == "__main__":
    main()