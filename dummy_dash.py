# This is just a driver for running the dash script off of a previously generated telemetry log

from time import sleep

import carstat


def parse_data(data, data_types) -> dict:
    
    return_dict = {}

    # For each data type, get size and then collect
    i = 0
    for key in data_types:
        # Join the key from the data_types dict with the values from the current data
        return_dict[key] = data[i]

        i += 1

    return return_dict

def main() -> None:
    # Read in data types from file
    data_types = {}
    with open("data_formats.txt", "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            data_types[line.split()[1]] = line.split()[0]

    print("Speed | RPM | Gear")
    with open("telemetry_log.tsv", "r") as data:
        for line in data:
            cols = line.split("\t")
            returned_data = parse_data(cols, data_types)
            telemetry = carstat.telemetry(returned_data)
            print(
                f"{int(float(telemetry.speed))} | {int(float(telemetry.rpm))} | {str(telemetry.gear)}",
                end="\r",
            )
            sleep(0.05)

            f"{int(telemetry.speed)} | {int(telemetry.rpm)} | {str(telemetry.gear)}",
            end="\r",


if __name__ == "__main__":
    main()
