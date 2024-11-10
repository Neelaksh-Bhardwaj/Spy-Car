import socket
from datetime import datetime

# Set up the server to listen for incoming UDP messages
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
server_address = ('', 5000)  # Listen on all interfaces on port 65432
server_socket.bind(server_address)

print("Waiting for messages...")

while True:
    data, address = server_socket.recvfrom(1024)  # Buffer size is 1024 bytes
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp
    print(f"{timestamp} - Received message: {data.decode()} from {address}")
