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
