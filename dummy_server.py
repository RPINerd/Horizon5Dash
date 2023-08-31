"""
    Dummy Telemetry Server | RPINerd 08/29/23

    Rethinking the way to handle doing "dry runs" for dev testing.

    The main dumping script option will dump the raw binary data packets
    into a pickle file as an iterable

    Dummy server simply loops over this list and sends each packet via UDP
    to a provided address/port as if Forza was actually running.
    Also can provide a time delay to wait between packets.
"""

import argparse
import pickle
import socket


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dummy Telemetry Server")
    parser.add_argument(
        "--ip",
        "-i",
        type=str,
        default="127.0.0.1",
        help="IP address to send the telemetry data to",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=10000,
        help="Port to send the telemetry data to",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default="dummy_telemetry.pkl",
        help="File to read the telemetry data from",
    )


def main(args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((args.ip, args.port))

    with open(args.file, "rb") as f:
        packet_list = pickle.load(f)

    # TODO need a graceful way to shutdown the server
    while True:
        for packet in packet_list:
            sock.sendto(packet, (args.ip, args.port))


if __name__ == "__main__":
    args = parse_args()
    main(args)
