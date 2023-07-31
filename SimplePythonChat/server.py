import socket
import threading

HOST = "127.0.0.1"
PORT = 12345
BUFFER_SIZE = 4096
clients = []
lock = threading.Lock()

def broadcast(message, sender=None):
    with lock:
        for client_socket in clients:
            if client_socket != sender:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error broadcasting message: {e}")
                    remove_client(client_socket)

def handle_client(client_socket, client_address):
    with lock:
        clients.append(client_socket)

    print(f"New connection from {client_address}")

    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            message = data.decode()
            if len(message) > 512:
                message = message[:512]
            print(f"User> {message}")
            broadcast(f"User> {message}", client_socket)

    except ConnectionResetError:
        print(f"Client {client_address} disconnected.")
    except socket.error as e:
        print(f"Error with client {client_address}: {e}")
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        with lock:
            remove_client(client_socket)
            print(f"Disconnected from {client_address}")

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected with {client_address}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
    except Exception as e:
        print(f"Error starting the server: {e}")

if __name__ == "__main__":
    start_server()
