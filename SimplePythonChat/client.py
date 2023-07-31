import socket
import threading

HOST = "127.0.0.1"  #Replace with the server IP
PORT = 12345
BUFFER_SIZE = 1024

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            message = data.decode()
            print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == "exit":
            break

        try:
            if len(message) > 512:
                message = message[:512]
            client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
