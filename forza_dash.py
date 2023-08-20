# Forza Dash
# A simple app for Forza Horizon 5 that can recieve the in-game telemetry
# and display it in real time in a customizable dashboard.
#

import argparse
import socket
import struct
from time import sleep

import carstat
import dummy_dash

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Forza Dash")
    parser.add_argument(
        "--ip",
        "-i",
        type=str,
        default="192.168.0.126",
        help="IP address of the telemetry server",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=10000,
        help="Port of the telemetry server",
    )
    run_type = parser.add_mutually_exclusive_group(required=False)
    run_type.add_argument(
        "--log",
        "-l",
        action="store_true",
        default=False,
        help="Dump the telemetry data to a log file",
    )
    run_type.add_argument(
        "--dryrun",
        "-d",
        action="store_true",
        default=False,
        help="Run the program without connecting to a telemetry server",
    )

    return parser.parse_args()


def get_data(data, data_types) -> dict:
    return_dict = {}

    # Additional var
    passed_data = data

    # For each data type, get size and then collect
    for key in data_types:
        d_type = data_types[key]
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


def main(args) -> None:
    # Read in data types from file
    data_types = {}
    with open("data_formats.txt", "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            data_types[line.split()[1]] = line.split()[0]

    # Establish connection to the telemetry output
    sock = open_socket(str(args.ip), 10000)

    # Open log file if needed
    if args.log:
        log_file = open("telemetry_log.tsv", "w")

    print("Speed | RPM | Gear")

    # Primary loop
    while True:
        # Recieve incoming data
        data, address = sock.recvfrom(1500)

        # Convert recieved data to a dictionary
        returned_data = get_data(data, data_types)

        # Create a carstat object with the parsed data
        telemetry = carstat.telemetry(returned_data)

        # Write all items in returned_data to a telemetry log file, tab delimited
        if args.log:
            for key in returned_data:
                log_file.write(str(returned_data[key]) + "\t")
            log_file.write("\n")

        # Print some small monitoring data
        print(
            f"{int(telemetry.speed)} | {int(telemetry.rpm)} | {str(telemetry.gear)}",
            end="\r",
        )


if __name__ == "__main__":

    args = parse_args()
    
    if args.dryrun:
        dummy_dash.main()
    else:
        main(args)
