# Forza Dash
# A simple app for Forza Horizon 5 that can recieve the in-game telemetry
# and display it in real time in a customizable dashboard.
#

import socket
import struct
import sys

import carstat

# Assigning sizes in bytes to each variable type
BYTESKU = {
    "s32": 4,  # Signed 32bit int, 4 bytes of size
    "u32": 4,  # Unsigned 32bit int
    "f32": 4,  # Floating point 32bit
    "u16": 2,  # Unsigned 16bit int
    "u8": 1,  # Unsigned 8bit int
    "s8": 1,  # Signed 8bit int
    "hzn": 12,  # Unknown, 12 bytes of.. something
}


def get_data(data):
    return_dict = {}

    # Additional var
    passed_data = data

    # For each data type, get size and then collect
    for key in data:
        d_type = data[key]
        size = BYTESKU[d_type]
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


def open_socket(server_address, port) -> socket.socket:
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    sock.bind((server_address, port))

    return sock


def main():
    # Read in data types from file
    data_types = {}
    with open("data_formats.txt", "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            data_types[line.split()[1]] = line.split()[0]

    # Establish connection to the telemetry output
    print("Establishing Socket...")
    sock = open_socket("localhost", 1337)

    # Primary loop
    while True:
        # Recieve incoming data
        data, address = sock.recvfrom(1500)

        print(data)
        print(address)

        # Convert recieved data to a dictionary
        returned_data = get_data(data, data_types)

        # Create a carstat object with the parsed data
        telemetry = carstat.CarStat(returned_data)

        print(f"Speed: {telemetry.speed}\nRPM: {telemetry.currentEngineRpm}\n")


if __name__ == "__main__":
    main()
