# Functions for displaying and updating the dashboard


import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot(telemetry) -> None:

    plt.style.use("fivethirtyeight")

    x_vals = []
    y_vals = []

    def animate(i):
        x_vals.append(telemetry.timestamp)
        y_vals.append(telemetry.rpm)

        plt.plot(x_vals, y_vals)
        return x_vals, y_vals

    ani = animation.FuncAnimation(plt.gcf(), animate, interval=20, frames=100)

    plt.tight_layout()
    plt.show()
