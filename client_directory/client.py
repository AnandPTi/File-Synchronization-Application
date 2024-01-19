import socket
import os
import struct

# Define server parameters
HOST = '127.0.0.1'
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Directory to synchronize on the client side
CLIENT_DIRECTORY = 'client_directory'

# Function to receive a file from the server
def receive_file(server_socket, file_path):
    # Receive the file size from the server
    file_size_data = server_socket.recv(8)
    file_size = struct.unpack("!Q", file_size_data)[0]

    # Receive the file data from the server in larger chunks
    chunk_size = 1024 * 1024  # 1 MB chunks
    file_data = b''
    remaining_size = file_size
    while remaining_size > 0:
        data = server_socket.recv(min(chunk_size, remaining_size))
        file_data += data
        remaining_size -= len(data)

    # Write the received data to the client file
    with open(file_path, 'wb') as f:
        f.write(file_data)

# Function to synchronize with the server
def sync_with_server():
    print("Synchronizing with the server...")

    # Receive the list of files from the server
    server_files = eval(client_socket.recv(1024).decode())

    # Synchronize files with the server
    for file in server_files:
        client_file_path = os.path.join(CLIENT_DIRECTORY, file)
        receive_file(client_socket, client_file_path)

    print("Synchronization completed.")

# Synchronize with the server
sync_with_server()

# Close the connection
client_socket.close()
