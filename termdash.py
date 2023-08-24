# Initialize the terminal based dashboard
def build():
    print("Speed | RPM | Gear")


def update(telemetry_window):
    # Get the most recent telemetry object
    telemetry = telemetry_window[-1]

    # Print some small monitoring data
    print(
        f"{int(telemetry.speed)} | {int(telemetry.rpm)} | {str(telemetry.gear)}",
        end="\r",
    )
