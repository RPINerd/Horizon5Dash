# This is just a test script to generate a batch of random data in the form 
# of a dictionary that will be sent out every 50 ms to visualization program.

import random
import time
import json
import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 8000)
sock.bind(server_address)

# Create a dictionary to hold the data
data = {}

# Create a list of keys
keys = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']

# Create a list of values
values = [0, 0, 0, 0, 0, 0]

# While loop to generate random data
while True:
    # Generate random data
    for i in range(len(values)):
        values[i] = random.uniform(-1, 1)

    # Create the dictionary
    data = dict(zip(keys, values))

    # Convert the dictionary to JSON
    json_data = json.dumps(data)

    # Send the data
    sock.sendto(json_data.encode(), ('localhost', 10000))

    # Sleep for 50 ms
    time.sleep(0.05)
    
