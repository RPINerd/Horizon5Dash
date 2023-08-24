# Forza Dash
# A simple app for Forza Horizon 5 that can recieve the in-game telemetry
# and display it in real time in a customizable dashboard.
#

import argparse

import carstat
import dashboard
import dummy_dash
import termdash
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
    parser.add_argument(
        "--window",
        "-w",
        type=int,
        default=100,
        help="Number of historical data points to display in the dashboard",
    )
    parser.add_argument(
        "--cli",
        "-c",
        action="store_true",
        default=False,
        help="Display the telemetry data in the command line",
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


def main(args, data_types) -> None:
    # Establish connection to the telemetry output
    sock = utils.open_socket(str(args.ip), 10000)

    # Print a command line header for the monitoring data
    if args.cli:
        termdash.build()

    # Sliding window for telemetry data
    telemetry_window = []

    # Primary loop
    while True:
        # Recieve incoming data
        data, address = sock.recvfrom(1500)

        # Convert recieved data to a dictionary
        returned_data = utils.get_data(data, data_types)

        # Create a carstat object with the parsed data
        telemetry = carstat.telemetry(returned_data)

        # For a user definable spread of datapoints, build up a list of telemetry objects as
        # data is streamed in. Once the list reaches the defined length, remove the oldest item
        # when adding the next item. This allows for a rolling window of data to be displayed.
        if len(telemetry_window) < args.window:
            telemetry_window.append(telemetry)
        else:
            telemetry_window.pop(0)
            telemetry_window.append(telemetry)

        # Send telemetry to the desired ouput
        if not args.cli:
            dashboard.plot(telemetry_window)
        else:
            termdash.update(telemetry_window)


if __name__ == "__main__":
    args = parse_args()

    # Read in data types from file
    # ? Over engineered for use with only 1 game, but good for future expansion
    data_types = utils.get_datatypes()

    if args.dryrun:
        dummy_dash.main(args, data_types, "run")
    elif args.dump:
        dummy_dash.main(args, "dump")
    else:
        main(args, data_types)
