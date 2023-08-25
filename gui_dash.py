"""
    Functions for running the GUI based dashboard
"""

import matplotlib.animation as animation
import matplotlib.pyplot as plt

# import numpy as np
# import pandas as pd
import utils


def main(args, sock, data_types) -> None:
    plt.style.use("fivethirtyeight")

    # Sliding window for telemetry data
    telemetry_window = []

    while True:
        # Get the data from the socket
        telemetry_window = utils.recieve_telemetry(sock, data_types, telemetry_window, args.window)

        # Get the most recent telemetry data
        telemetry = telemetry_window[-1]

        x_vals = [telemetry[i].timestamp for i in range(len(telemetry))]
        y_vals = [telemetry[i].rpm for i in range(len(telemetry))]

        def animate(i):
            x_vals.append(telemetry.timestamp)
            y_vals.append(telemetry.rpm)

            plt.cla()
            plt.plot(x_vals, y_vals)

            plt.legend(loc="upper left")
            plt.tight_layout()

            return x_vals, y_vals

        ani = animation.FuncAnimation(plt.gcf(), animate, interval=20, frames=100)
        plt.plot(x_vals, y_vals)
        plt.tight_layout()
        plt.show()
