# Forza Dash
# A simple app for Forza Horizon 5 that can recieve the in-game telemetry
# and display it in real time in a customizable dashboard.
#

import sys
import socket
import json

# Open a socket to recieve the telemetry data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)

# Recieve incoming data
data, address = sock.recvfrom(4096)

# Decode the data
data = data.decode()

# Convert the data to a dictionary
data = json.loads(data)

# Print the data
print(data)
