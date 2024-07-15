import socket as so
import threading 

HOST = "190.169.1.135" # This is only a random IP
PORT = 3000
LISTEN_LIMIT = 10
active_clients = [] # List of all currently connected clients

def messages_from_server(client, username):
    
   while 1:
        
     message = client.recv(2048).decode("utf-8")
     if message != " ":
         final_message = username + "~" + message
         send_messages_to_all(final_message)
         
     else:
        print(f"The message send from client{username}is empty")
         
         
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
    
        # Server will listen for client messages that
        # will contain the username
        while 1:
            
            username = client.recv(2048).decode("utf-8")
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
        
    except ConnectionRefusedError as error:
        print(f"It´s not possible to bind to host {HOST} and to port {PORT}",error)

    server.listen(LISTEN_LIMIT)
    
    # This loop will listen for all possible client connections to the chat
    while 1:
        
       client, address = server.accept()
       print(f"Succesfully connected to client {address[0]} {address[1]}")
       threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == "__main__":
    main()
