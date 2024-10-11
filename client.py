import socket as so
import threading 

HOST = "190.169.1.135" 
PORT = 5000


def messages_from_server(client):
    # Recibe y muestra mensajes del servidor
    try:
        while True:
            message = client.recv(1024).decode("utf-8")
            if message.strip():  # Verifica que el mensaje no esté vacío
                username, content = message.split("~", 1)
                print(f"[{username}] {content}")
            else:
                print("Received an empty message from the server.")
    
      except (ConnectionResetError, ConnectionAbortedError):
            print("Connection lost. Exiting.")
      except Exception as e:
            print(f"An error occurred while receiving message: {e}")
      finally:
            client.close()

def send_message_to_server(client):
    # Envía mensajes de entrada del usuario al servidor
    try:
        while True:
            message = input("Message: ").strip()
            if message:
                client.sendall(message.encode())
            else:
                print("Empty message. Type something to send.")
                
    except (ConnectionResetError, ConnectionAbortedError):
        print("Connection lost. Unable to send message.")
    except Exception as e:
        print(f"An error occurred while sending message: {e}")
    finally:
        client.close()


def communicate_to_server(client):
    
   try:
        username = input("Enter your username: ").strip()
        if username:
            client.sendall(username.encode())
        else:
            print("Username cannot be empty. Exiting.")
            client.close()
            return
        threading.Thread(target=messages_from_server, args=(client,), daemon=True).start()
        send_message_to_server(client)
    except (ConnectionResetError, ConnectionAbortedError):
        print("Connection error occurred. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
    

        
if __name__ == "__main__":
    main()

