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
    while True:

        # Break the loop when the user presses Ctrl+C
        try:
            pass
        except KeyboardInterrupt:
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

        sleep(0.01)
    
    # Once the loop is broken, write the pickle_list to a file
    with open("telemetry_log.pkl", "wb") as pkl:
        pickle.dump(pickle_list, pkl)


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
        print("Speed | RPM | Gear")
        with open("telemetry_log.tsv", "r") as data:
            for line in data:
                cols = line.split("\t")
                returned_data = utils.parse_data(cols, data_types)
                telemetry = carstat.telemetry(returned_data)
                dashboard.plot(telemetry)
                print(
                    f"{int(float(telemetry.speed))} | {int(float(telemetry.rpm))} | {str(telemetry.gear)}",
                    end="\r",
                )
                sleep(0.01)
        return
    
    else:
        print("Invalid task")
        return
