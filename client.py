import socket as so
import threading 
import zlib
import logging
import time

HOST = "190.169.1.135" 
PORT = 5000
TIMEOUT = 10
RETRY_DELAY = 2  # Segundos de espera entre intentos de reconexión
MAX_RETRIES = 3  # Máximo de intentos de reconexión

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def compress_message(message):
    # Comprime el mensaje usando zlib
    return zlib.compress(message.encode())

def decompress_message(message):
    # Descomprime el mensaje usando zlib
    return zlib.decompress(message).decode()

def messages_from_server(client):
    # Recibe y muestra mensajes del servidor
    try:
        while True:
            message = client.recv(1024).decode("utf-8")
            if message.strip():  # Verifica que el mensaje no esté vacío
                username, content = message.split("~", 1)
                logging.info(f"[{username}] {content}")
            else:
                logging.warning("Received an empty message from the server.")
    
      except (ConnectionResetError, ConnectionAbortedError):
            logging.error("Connection lost. Exiting.")
      except Exception as e:
            logging.error(f"An error occurred while receiving message: {e}")
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
        logging.error("Connection lost. Unable to send message.")
    except Exception as e:
        logging.error(f"An error occurred while sending message: {e}")
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
        logging.error("Connection error occurred. Exiting.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        client.close()
    
def connect_with_retries():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            with so.socket(so.AF_INET, so.SOCK_STREAM) as client:
                client.settimeout(TIMEOUT)
                logging.info(f"Connecting to {HOST}:{PORT} (Attempt {retries + 1})")
                client.connect((HOST, PORT))
                communicate_to_server(client)
                break  # Exit loop if connection is successful
        except (so.timeout, so.error) as e:
            retries += 1
            logging.warning(f"Connection attempt {retries} failed: {e}")
            if retries < MAX_RETRIES:
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logging.error("Max retries reached. Could not connect to the server.")
        
if __name__ == "__main__":
     try:
        with so.socket(so.AF_INET, so.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.settimeout(TIMEOUT)
            communicate_to_server(client)
    except so.error as e:
        print(f"Could not connect to the server: {e}")

    connect_with_retries()
