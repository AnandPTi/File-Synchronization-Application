import socket
import os
import threading
import struct

# Define server parameters
HOST = '127.0.0.1'
PORT = 12345
DIRECTORY_TO_SYNC = 'server_directory'

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# List to store connected clients
clients = []

# Lock to synchronize access to the shared directory
lock = threading.Lock()

# Function to send a file to a client
def send_file(client_socket, file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()

        # Send the file size to the client
        file_size = len(file_data)
        client_socket.sendall(struct.pack("!Q", file_size))

        # Send the file data to the client in larger chunks
        chunk_size = 1024 * 1024  # 1 MB chunks
        for i in range(0, len(file_data), chunk_size):
            client_socket.sendall(file_data[i:i + chunk_size])

# Function to synchronize with a client
def sync_with_client(client_socket):
    with lock:
        # List all files in the server directory
        files_to_sync = [f for f in os.listdir(DIRECTORY_TO_SYNC) if os.path.isfile(os.path.join(DIRECTORY_TO_SYNC, f))]

        # Send the list of files to the client
        client_socket.send(str(files_to_sync).encode())

        # Synchronize files with the client
        for file in files_to_sync:
            file_path = os.path.join(DIRECTORY_TO_SYNC, file)
            send_file(client_socket, file_path)

        print("Synchronization completed.")

    # Signal the end of synchronization
    client_socket.sendall(b'Done')

# Function to handle client connections
def handle_client(client_socket):
    try:
        while True:
            sync_with_client(client_socket)
    except:
        pass
    finally:
        # Remove the client when disconnected
        clients.remove(client_socket)
        client_socket.close()

# Listen for incoming connections
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

# Accept and handle client connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Add the new client to the list
    clients.append(client_socket)

    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
