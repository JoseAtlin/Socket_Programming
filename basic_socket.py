import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("Socket creation failure with an error {}".format(err))

port = 80
try:
    host_ip = socket.gethostbyname("www.google.com")
except socket.gaierror:
    print("Error when trying to connect to the host")
    sys.exit()

s.connect((host_ip, port))
print("The socket has successfully connected to google on port {}".format(host_ip))