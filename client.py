import socket
import threading


def client_receive():
    while 1:
        person = c.recv(1).decode('utf-8')
        if person == '1' or person == '2':
            s_l = c.recv(4).decode('utf-8')
            receiver = c.recv(int(s_l)).decode('utf-8')
            m_l = c.recv(16).decode('utf-8')
            msg = c.recv(int(m_l)).decode('utf-8')
            time = c.recv(8).decode('utf-8')
            print(receiver, '-' * 5, msg, '-' * 5, time)
            print()
        elif person == '3':
            msg = c.recv(17).decode('utf-8')
            time = c.recv(8).decode('utf-8')
            print("status : ", msg, '-'*5, time)
            print()
        elif person == '4':
            msg = c.recv(21).decode('utf-8')
            time = c.recv(8).decode('utf-8')
            print("status : ", msg, '-'*5, time)
            print()


def client_send(receiver, msg):
    send_message = msg.encode('utf-8')
    receiver = receiver.encode('utf-8')
    sender = name.encode('utf-8')
    msg_length = str(len(send_message)).encode('utf-8')
    msg_length += b' ' * (16 - len(msg_length))
    c.send(msg_length)
    c.send(send_message)
    sender_length = str(len(sender)).encode('utf-8')
    sender_length += b' ' * (4 - len(sender_length))
    c.send(sender_length)
    c.send(sender)
    receiver_length = str(len(receiver)).encode('utf-8')
    receiver_length += b' ' * (4 - len(receiver_length))
    c.send(receiver_length)
    c.send(receiver)


PORT = 6060
SERVER = "127.0.1.1"
server_messages = []                                # [[sender, receiver , message, time],......]
conn_name_dict = {}                                 # {(connection : sender_name)......}
conn_ip_dict = {}                                   # {(connection : ip_address).......}


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((SERVER, PORT))
th = threading.Thread(target=client_receive)
th.start()
name = (input("Enter Your Name : ")).upper()
notice_length = str(len(name)).encode('utf-8')
notice_length += b' ' * (4 - len(notice_length))
c.send(notice_length)
c.send(name.encode('utf-8'))
print("[CONNECTED] TO SERVER : {} AS {}".format(SERVER, name))

while 1:
    print("\nDo you want to ::\n1.Broadcast\n2.Personal")
    print("To quit using Broadcast or Personal, type \"quit\"")
    option = int(input("Enter your Option : "))
    if option == 1:
        print("\n-----> Message Format ::\n-----> 1st line : Message\n")
    else:
        print("\n-----> Message Format ::\n-----> 1st line : Receiver's Name\n-----> 2nd line : Message\n")

    while 1:
        if option == 1:
            to_whom = "everyone".upper()
        else:
            to_whom = input().upper()
        if to_whom == "":
            continue
        if to_whom == "quit":
            break
        type_here = input()
        if type_here == "":
            continue
        if type_here == "quit":
            break
        client_send(to_whom, type_here)
