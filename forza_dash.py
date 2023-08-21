# Forza Dash
# A simple app for Forza Horizon 5 that can recieve the in-game telemetry
# and display it in real time in a customizable dashboard.
#

import argparse

import carstat
import dashboard
import dummy_dash
import utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Forza Dash")
    parser.add_argument(
        "--ip",
        "-i",
        type=str,
        default="127.0.0.1",
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
        "--dump",
        "-o",
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


def main(args) -> None:
    
    data_types = utils.get_datatypes()

    # Establish connection to the telemetry output
    sock = utils.open_socket(str(args.ip), 10000)

    print("Speed | RPM | Gear")

    # Primary loop
    while True:
        # Recieve incoming data
        data, address = sock.recvfrom(1500)

        # Convert recieved data to a dictionary
        returned_data = utils.get_data(data, data_types)

        # Create a carstat object with the parsed data
        telemetry = carstat.telemetry(returned_data)

        #dashboard.update(telemetry)

        # Print some small monitoring data
        print(
            f"{int(telemetry.speed)} | {int(telemetry.rpm)} | {str(telemetry.gear)}",
            end="\r",
        )


if __name__ == "__main__":

    args = parse_args()
    
    if args.dryrun:
        dummy_dash.main(args, "run")
    elif args.dump:
        dummy_dash.main(args, "dump")
    else:
        main(args)
