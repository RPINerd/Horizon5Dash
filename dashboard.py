# Functions for displaying and updating the dashboard

import tkinter as tk

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def plot() -> None:
    fig, ax = plt.subplots()

    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))


    def animate(i):
        line.set_ydata(np.sin(x + i / 50))  # update the data.
        return line,


    ani = animation.FuncAnimation(
        fig, animate, interval=20, blit=True, save_count=50)

    plt.show()
        
# Create the dashboard window
def build() -> None:

    # Create the window
    window = tk.Tk()
    
    # Create the speedometer
    speedometer = tk.Canvas(window, width=200, height=200)
    speedometer.pack()

    # Create the tachometer
    tachometer = tk.Canvas(window, width=200, height=200)
    tachometer.pack()

    # Create the gear indicator
    gear = tk.Canvas(window, width=200, height=200)
    gear.pack()

    # Create the brake indicator
    brake = tk.Canvas(window, width=200, height=200)
    brake.pack()

    # Create the throttle indicator
    throttle = tk.Canvas(window, width=200, height=200)
    throttle.pack()
    
    # Create the steering indicator
    steering = tk.Canvas(window, width=200, height=200)
    steering.pack()

    # Create the clutch indicator
    clutch = tk.Canvas(window, width=200, height=200)
    clutch.pack()

    # Create the handbrake indicator
    handbrake = tk.Canvas(window, width=200, height=200)
    handbrake.pack()

    # Create the ABS indicator
    abs = tk.Canvas(window, width=200, height=200)
    abs.pack()
    
    # Launch the window
    window.mainloop()


def update(telemetry) -> None:
    pass