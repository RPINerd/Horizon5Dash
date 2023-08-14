# Forza Dash
# A simple app for Forza Horizon 5 that can recieve the in-game telemetry
# and display it in real time in a customizable dashboard.
#

import json
import socket
import sys

# Read in data types from file
data_types = {}
with open("data_formats.txt", "r") as f:
    lines = f.read().split("\n")
    for line in lines:
        data_types[line.split()[1]] = line.split()[0]


def get_data(data):
    return_dict = {}

    # Additional var
    passed_data = data

    # For each data type, get size and then collect
    for key in data_types:
        d_type = data_types[key]
        size = byte_skus[d_type]
        current = passed_data[:size]

        decoded = 0
        # Decoding for each type of data
        if d_type == "s32":
            decoded = int.from_bytes(current, byteorder="little", signed=True)
        elif d_type == "u32":
            decoded = int.from_bytes(current, byteorder="little", signed=False)
        elif d_type == "f32":
            decoded = struct.unpack("f", current)[0]
        elif d_type == "u16":
            decoded = struct.unpack("H", current)[0]
        elif d_type == "u8":
            decoded = struct.unpack("B", current)[0]
        elif d_type == "s8":
            decoded = struct.unpack("b", current)[0]

        # Add decoded data to the dict
        return_dict[key] = decoded

        # Remove the already read bytes from the variable
        passed_data = passed_data[size:]

    return return_dict


# Open a socket to recieve the telemetry data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ("localhost", 10000)
sock.bind(server_address)

# Recieve incoming data
data, address = sock.recvfrom(4096)

# Decode the data
data = data.decode()

# Convert the data to a dictionary
data = json.loads(data)

# Print the data
print(data)
