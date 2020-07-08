# Socket_Programming

![alt text](https://github.com/JoseAtlin/Socket_Programming/blob/master/socket_programming.png?raw=true)

**basic_socket** - Creating a socket and connecting to a server (here eg: www.google.com).

**simple_server_client** - Creating a socket which creates the localhost as the server with a port (5050). Using diff ports as the client sockets to connect to the Server. Clients can send messages to the server and the server keeps listening. This is an example of one-way connection between the clients and server. here the server doesnot send back messages.

**messaging_sockets** - This is a completely functional Server client Messaging application. Here blocks of data is send from client to server. Since I am introducing both broadcast(sending message to all other clients) and personal(sending to a specified person only). The buffer size needs to be mentioned beforehand.
And that is why the message along with the buffer size is send together always. Also to note that, every time the client sends the message the message along with the sender_name, receiver_name, time, message will be stored in the server as server_messages list. Also there is couple of dictionaries to keep track of the ip-address aong with the name to know which person is which.
