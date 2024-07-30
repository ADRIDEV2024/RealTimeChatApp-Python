import socket as so
import threading 

HOST = "190.169.1.135" # This is only a random IP
PORT = 3000

def messages_from_server(client):
    
   while True:
        
     message = client.recv(1024).decode("utf-8")
     if message != "":
         username = message.split("~")[0]
         print(f"[{username}] {content}")
         
     else:
        print("Message recevied from client is empty")
        
def send_message_to_server(client):
    
    while True:
        
        message = input("Message: ")
        if message != " ":
            client.sendall(message.encode())
        else:
            print("Message is empty")
            exit(0)

def communicate_to_server(client):
    
    username = input("Enter your username: ")
    if username != " ":
        client.sendall(username.encode())
    else:
        print("Oopss, the username can´t be empty")
        exit(0)
    threading.Thread(target=messages_from_server, args=(client, )).start()

    
def main():
    
    server = so.socket(so.AF_INET, so.SOCK_STREAM)
    
    try:
        server.connect((HOST,PORT))
        print("Succesfull connection to the server")
        
    except ConnectionRefusedError as error:
        print(f"Unable to connect to server {HOST},{PORT}",error)
        
if __name__ == "__main__":
    main()

