import socket as so
import select
import json
import logging
import threading 

HOST = "190.169.1.135"
PORT = 5000
LISTEN_LIMIT = 10
ACTIVE_CLIENTS = [] 
BUFFER_SIZE = 1024

class ChatServer:
    def __init__(self):
        self.server_socket = None
        self.client_sockets = []
        self.clients = {}

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(LISTEN_LIMIT)
            logger.info(f"Server is running on {HOST}:{PORT}")
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return
        
        self.client_sockets.append(self.server_socket)

        while True:
            try:
                read_sockets, _, exception_sockets = select.select(self.client_sockets, [], self.client_sockets)

                for notified_socket in read_sockets:
                    if notified_socket == self.server_socket:
                        self.accept_new_connection()
                    else:
                        self.handle_client_message(notified_socket)

                for notified_socket in exception_sockets:
                    self.remove_client(notified_socket)

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                
def accept_new_connection(self):
        client_socket, client_address = self.server_socket.accept()
        if len(self.clients) >= LISTEN_LIMIT:
            client_socket.send("Server is full".encode('utf-8'))
            client_socket.close()
            return

        username = self.receive_message(client_socket)
        if not username:
            return

        self.clients[client_socket] = username
        self.client_sockets.append(client_socket)
        logger.info(f"New connection from {client_address}, username: {username}")
        self.broadcast_message(f"{username} has joined the chat!")

         
def send_messages_to_client(client, message):
      client.sendall(message.encode())

def send_messages_to_all(message):
    """
    Function to send any new message to all the clients
    that are currently connected to this server
    """
    
    for user in active_clients:
        send_messages_to_client(user[1], message)

def client_handler(client):
    
        while 1:
            
            username = client.recv(2048).decode("latin")
            if username != " ":
                active_clients.append((username, client))
                break
            else:
                print("Client username is empty")
        threading.Thread(target=messages_from_server, args=(client, username)).start()
              
def main():
    # Creating the socket object
    server = so.socket(so.AF_INET, so.SOCK_STREAM)
    # AF_INET for IPv4 addresses and SOCK_STREAM for TCP communications
    
    try:
        server.bind((HOST,PORT))
        print("Server is running !")
        
    except ConnectionRefusedError as exception:
        print(f"It´s not possible to bind to host {HOST} and to port {PORT}",exception)

    server.listen(LISTEN_LIMIT)
    
    # This loop will listen for all possible client connections to the chat
    while 1:
        
       client, address = server.accept()
       print(f"Succesfully connected to client {address[0]} {address[1]}")
       threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == "__main__":
    main()
