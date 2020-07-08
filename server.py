import socket
import threading
from datetime import datetime


def start():
    s.listen()
    print("[LISTENING]...server : {}".format(SERVER))
    while 1:
        conn, address = s.accept()
        thread = threading.Thread(target=client_server, args=(conn, address))
        thread.start()
        conn_ip_dict[conn] = address
        print("[ACTIVE CONNECTIONS] : ", len(conn_ip_dict))


def client_server(conn, address):
    print("[NEW CONNECTION] : {}".format(address))
    length = conn.recv(4).decode('utf-8')
    client = conn.recv(int(length)).decode('utf-8')
    conn_name_dict[conn] = client
    online.add(client)
    while 1:
        msg_length = conn.recv(16).decode('utf-8')
        if msg_length:
            message_details = []                                            # [sender, receiver, message, time]
            msg = conn.recv(int(msg_length)).decode('utf-8')
            sender_length = conn.recv(4).decode('utf-8')
            sender = conn.recv(int(sender_length)).decode('utf-8')
            receiver_length = conn.recv(4).decode('utf-8')
            receiver = conn.recv(int(receiver_length)).decode('utf-8')
            time = datetime.now().strftime("%I:%M:%P")
            message_details.extend((sender, receiver, msg, time))
            server_messages.append(message_details)
            if msg == "DISCONNECT":
                print("[{}] : DISCONNECTED".format(address))
                conn.close()
                del conn_name_dict[conn]
                online.remove(sender)
                break
            print(message_details)
            server_send(conn, sender, receiver, msg, time)


def server_send(conn, sender, receiver, msg, time):
    if receiver == "EVERYONE" or receiver in online:
        for socks in conn_name_dict:
            if conn_name_dict[socks] != sender:
                if receiver == "EVERYONE":
                    socks.send('1'.encode('utf-8'))
                    s_l = str(len(sender)).encode('utf-8')
                    s_l += b' ' * (4 - len(s_l))
                    socks.send(s_l)
                    socks.send(sender.encode('utf-8'))
                    m_l = len(msg)
                    m_l = str(m_l).encode('utf-8')
                    m_l += b' ' * (16 - len(m_l))
                    socks.send(m_l)
                    socks.send(msg.encode('utf-8'))
                    socks.send(time.encode('utf-8'))
                else:
                    if conn_name_dict[socks] == receiver:
                        socks.send('2'.encode('utf-8'))
                        s_l = str(len(sender)).encode('utf-8')
                        s_l += b' ' * (4 - len(s_l))
                        socks.send(s_l)
                        socks.send(sender.encode('utf-8'))
                        m_l = str(len(msg)).encode('utf-8')
                        m_l += b' ' * (16 - len(m_l))
                        socks.send(m_l)
                        socks.send(msg.encode('utf-8'))
                        socks.send(time.encode('utf-8'))
            else:
                socks.send('3'.encode('utf-8'))
                socks.send("Message Delivered".encode('utf-8'))
                socks.send(time.encode('utf-8'))
    else:
        conn.send('4'.encode('utf-8'))
        conn.send("Message NOT Delivered".encode('utf-8'))
        conn.send(time.encode('utf-8'))


PORT = 6060
SERVER = socket.gethostbyname(socket.gethostname())
server_messages = []                                # [[sender, receiver , message, time],......]
conn_name_dict = {}                                 # {(connection : sender_name)......}
conn_ip_dict = {}                                   # {(connection : ip_address).......}
online = set()                                      # {online-user_names,.....}


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("[SERVER STARTING]...")
s.bind((SERVER, PORT))
t = threading.Thread(target=start)
t.start()
t.join()
