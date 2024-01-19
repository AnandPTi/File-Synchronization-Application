# File Synchronization Application

This is a simple client-server file synchronization application implemented in Python using socket programming. The application allows files to be synchronized between a central server and multiple client systems.

## Prerequisites

- Python 3.x installed on both the server and client machines.

## Setup

### Server Setup
 Run the server script:
   ```bash
   python server.py
   ```
   The server will start listening for incoming connections.
Place the files you want to synchronize in the `server_directory` folder.

### Client Setup

 Open a terminal and navigate to the directory containing `client.py`.

  Edit `client.py` to specify the IP address and port of the central server. By default:
   ```python
   HOST = '127.0.0.1'  # Change this to the IP address of your central server
   PORT = 12345         # Change this to the port used by your central server
   ```
  Run the client script:
   ```bash
   python client.py
   ```
   The client will connect to the central server and synchronize files.

Repeat the client setup on each machine that needs to synchronize with the central server.

## File Synchronization

- The server sends the list of files to each connected client.

- Clients update their local directories based on the synchronization process.

- Existing client files are updated, and new files on the server are transferred to clients.

## Customization

- Adjust the `HOST` and `PORT` variables in `client.py` to match the IP address and port of your central server.

- Customize the server and client directories as needed.

## Notes

- Ensure that the central server machine is accessible from all client machines.

- Consider network configurations and permissions to enable connectivity between the central server and clients.

- This is a basic example and may need additional enhancements for production use.

