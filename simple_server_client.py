import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handle_client(conn, addr):
    print("[NEW CONNECTION] {} connected...".format(addr))
    while 1:
        msg_length = conn.recv(16).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode('utf-8')
            if msg == "DISCONNECT":
                print("[{}] : DISCONNECTED".format(addr))
                break
            print("[{}] : {}".format(addr, msg))
    conn.shutdown(0)
    conn.close()


def start():
    s.listen()
    print("[LISTENING]...server : {}".format(SERVER))
    while 1:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[ACTIVE CONNECTIONS] : {}".format(threading.activeCount() - 1))


ch = int(input("1. Server\n2. Client\n"))
if ch == 1:
    print("[SERVER STARTING]...")
    s.bind((SERVER, PORT))
    start()
else:
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((SERVER, PORT))


def send(msg):
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (16 - len(send_length))
    c.send(send_length)
    c.send(message)


while 1:
    type_here = input("Enter Your Message : ")
    send(type_here)
    if type_here == "DISCONNECT":
        print("You've been successfully disconnected from the server")
        break
