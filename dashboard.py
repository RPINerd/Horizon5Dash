# Functions for displaying and updating the dashboard


import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot(telemetry) -> None:

    plt.style.use("fivethirtyeight")

    x_vals = [telemetry[i].timestamp for i in range(len(telemetry))]
    y_vals = [telemetry[i].rpm for i in range(len(telemetry))]

    # def animate(i):
    #     x_vals.append(telemetry.timestamp)
    #     y_vals.append(telemetry.rpm)

    #     plt.cla()
    #     plt.plot(x_vals, y_vals)

    #     plt.legend(loc="upper left")
    #     plt.tight_layout()

    #     return x_vals, y_vals

    # ani = animation.FuncAnimation(plt.gcf(), animate, interval=20, frames=100)
    plt.plot(x_vals, y_vals)
    plt.tight_layout()
    plt.show()
