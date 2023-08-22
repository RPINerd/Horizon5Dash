# This is just a driver for running the dash script off of a previously generated telemetry log

import pickle
from time import sleep

import carstat
import dashboard
import utils


def dump(ip, port, data_types) -> None:

    # Establish connection to the telemetry output
    sock = utils.open_socket(str(ip), port)

    pickle_list = []
    i = 0
    while True:

        if i == 3000:
            break

        # Recieve incoming data
        data, address = sock.recvfrom(1500)

        # Convert recieved data to a dictionary
        returned_data = utils.get_data(data, data_types)

        # Create a pickle of the returned data and append it to the pickle_list
        pickle_list.append(pickle.dumps(returned_data))

        # Write all items in returned_data to a telemetry log file, tab delimited
        # for key in returned_data:
        #     logfile.write(str(returned_data[key]) + "\t")
        # logfile.write("\n")

        i += 1
        print(i, end="\r")
        sleep(0.01)
    
    # Once the loop is broken, write the pickle_list to a file
    with open("telemetry_log.pkl", "wb") as pkl:
        pickle.dump(pickle_list, pkl)


def dryrun(window) -> None:

    # Parse the previously saved telemetry data from the pickle file
    with open("telemetry_log.pkl", "rb") as pkl:
        pickle_list = pickle.load(pkl)

    
    # Step through the pickle_list and plot the data as if it were live
    telemetry_window = []
    print("Speed | RPM | Gear")
    for tele_point in pickle_list:
        #cols = line.split("\t")
        #returned_data = utils.parse_data(cols, data_types)
        returned_data = pickle.loads(tele_point)
        telemetry = carstat.telemetry(returned_data)

        if len(telemetry_window) < window:
            telemetry_window.append(telemetry)
        else:
            telemetry_window.pop(0)
            telemetry_window.append(telemetry)

        dashboard.plot(telemetry_window)
        # print(
        #     f"{int(telemetry.speed)} | {int(telemetry.rpm)} | {telemetry.gear}",
        #     end="\r",
        # )
        sleep(0.01)


def main(args, task) -> None:
    
    # Read in data types from file
    data_types = {}
    with open("data_formats.txt", "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            data_types[line.split()[1]] = line.split()[0]

    if task == "dump":
        dump(args.ip, args.port, data_types)
        return
    
    elif task == "run":
        dryrun(args.window)
        return
    
    else:
        print("Invalid task")
        return
