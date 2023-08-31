"""
    Forza Dash | RPINerd, 08/25/23

    A simple app for Forza Horizon 5 that can recieve the in-game telemetry and display it
    in real time in a customizable dashboard.

"""

import argparse
import pickle
from time import sleep

import carstat
import gui_dash
import terminal_dash
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
        "-d",
        action="store_true",
        default=False,
        help="Dump the telemetry data to a log file",
    )
    # run_type.add_argument(
    #     "--dryrun",
    #     "-d",
    #     action="store_true",
    #     default=False,
    #     help="Run the program without connecting to a telemetry server",
    # )

    return parser.parse_args()


def dryrun(window) -> None:
    # Parse the previously saved telemetry data from the pickle file
    with open("telemetry_log.pkl", "rb") as pkl:
        pickle_list = pickle.load(pkl)

    # Step through the pickle_list and plot the data as if it were live
    telemetry_window = []
    print("Speed | RPM | Gear")
    for tele_point in pickle_list:
        # cols = line.split("\t")
        # returned_data = utils.parse_data(cols, data_types)
        returned_data = pickle.loads(tele_point)
        telemetry = carstat.telemetry(returned_data)

        if len(telemetry_window) < window:
            telemetry_window.append(telemetry)
        else:
            telemetry_window.pop(0)
            telemetry_window.append(telemetry)

        ui = gui_dash.build_ui()
        gui_dash.update_ui(ui)
        sleep(0.01)


def dump(sock, data_types) -> None:
    pickle_list = []
    i = 0
    while True:
        if i == 3000:
            break

        # Recieve incoming data
        data, address = sock.recvfrom(1500)

        # Convert recieved data to a dictionary
        # returned_data = utils.parse_data(data, data_types)

        # Create a pickle of the returned data and append it to the pickle_list
        pickle_list.append(pickle.dumps(data))

        i += 1
        print(i, end="\r")
        sleep(0.01)

    # Once the loop is broken, write the pickle_list to a file
    with open("telemetry.pkl", "wb") as pkl:
        pickle.dump(pickle_list, pkl)


def main(args) -> None:
    # Dryrun simulates the program running without a connection to the telemetry server.
    # Requires a pickle file of previously saved telemetry data!
    # if args.dryrun:
    #     dryrun(args.window)
    #     exit()

    # Read in data types from file
    # ? Over engineered for use with only 1 game, but good for future expansion
    data_types = utils.get_datatypes()

    # Establish connection to the telemetry output
    sock = utils.open_socket(str(args.ip), 10000)

    if args.dump:
        dump(sock, data_types)
    elif args.cli:
        terminal_dash.main(args, sock, data_types)
    else:
        gui_dash.main(args, sock, data_types)


if __name__ == "__main__":
    args = parse_args()
    main(args)
