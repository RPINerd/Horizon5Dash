"""
    Functions for running the terminal based dashboard
"""

from dashing import (
    ColorRangeVGauge,
    HBrailleChart,
    HBrailleFilledChart,
    HChart,
    HGauge,
    HSplit,
    Log,
    Text,
    VChart,
    VGauge,
    VSplit,
)

import utils


# Initialize the terminal based dashboard
def build_ui():
    column0 = VSplit(
        # RPM Gauge along the height of the left-most column
        ColorRangeVGauge(
            title="RPM: 100\tSpeed: 0 mph",
            val=0,
            border_color=2,
            colormap=(
                (85, 2),
                (90, 3),
                (97, 1),
            ),
        ),
    )

    column1 = VSplit(
        # Car info along the top
        Text("", title="Car Info", border_color=2, color=1),
        # Car positional information below that
        Text("", title="Positional", border_color=2, color=1),
        # Horizontal gauges along the bottom, summarizing control inputs
        HSplit(
            # Current speed and acceleration pedal position
            VGauge(title="Accel", val=0, border_color=2, color=2),
            # Brake pedal position
            VGauge(title="Brake", val=0, border_color=2, color=1),
            # Clutch pedal position
            VGauge(title="Clutch", val=0, border_color=2, color=3),
            # Handbrake position
            VGauge(title="Handbrake", val=0, border_color=2, color=4),
        ),
    )

    column2 = VSplit(
        HSplit(
            ColorRangeVGauge(title="Front Left", border_color=2, colormap=((80, 2), (90, 1))),
            ColorRangeVGauge(title="Front Right", border_color=2, colormap=((80, 2), (90, 1))),
        ),
        HSplit(
            ColorRangeVGauge(title="Rear Left", border_color=2, colormap=((80, 2), (90, 1))),
            ColorRangeVGauge(title="Rear Right", border_color=2, colormap=((80, 2), (90, 1))),
        ),
    )

    column3 = VSplit(
        Text("", title="Raw Telemetry", color=1),
    )

    # Dashing UI Construction
    ui = HSplit(column0, column1, column2, column3, title="Forza Dash")

    return ui


def main(args, sock, data_types):
    # Build the UI
    ui = build_ui()

    # Set some easy reference variables for the gauges

    # Column 0
    rpm = ui.items[0].items[0]

    # Column 1
    # Row 0
    info = ui.items[1].items[0]
    # Row 1
    positional = ui.items[1].items[1]
    # Row 2
    speed = ui.items[1].items[2].items[0]
    brake = ui.items[1].items[2].items[1]
    clutch = ui.items[1].items[2].items[2]
    handbrake = ui.items[1].items[2].items[3]

    # Column 2
    susp_norm_fl = ui.items[2].items[0].items[0]
    susp_norm_fr = ui.items[2].items[0].items[1]
    susp_norm_rl = ui.items[2].items[1].items[0]
    susp_norm_rr = ui.items[2].items[1].items[1]

    # Column 3
    raw = ui.items[3].items[0]

    # Sliding window for telemetry data
    telemetry_window = []

    while True:
        # Get the data from the socket
        telemetry_window = utils.recieve_telemetry(sock, data_types, telemetry_window, args.window)

        # Get the most recent telemetry data
        telemetry = telemetry_window[-1]

        # Column 0, RPM gauge
        rpm.title = f"RPM: {int(telemetry.rpm)}\tSpeed: {int(telemetry.speed)} mph"
        rpm.value = telemetry.normalized_rpm()

        # Column 1, Car info and positional information, and speed/brake gauges
        info.text = f"Class: {telemetry.carClass}\nPI: {telemetry.carPI}\nDrivetrain: {telemetry.drivetrainType}\nCylinders: {telemetry.numCylinders}\nGear: {telemetry.gear}\nPower: {telemetry.power} HP\nTorque: {telemetry.torque} lb/ft\nBoost: {telemetry.boost} psi"
        positional.text = f"Car Ordinal: {telemetry.carOrdinal}\nX: {telemetry.positionX}\nY: {telemetry.positionY}\nZ: {telemetry.positionZ}\nYaw: {telemetry.yaw}\nPitch: {telemetry.pitch}\nRoll: {telemetry.roll}"
        speed.value = telemetry.accel
        brake.value = telemetry.brake
        clutch.value = telemetry.clutch
        handbrake.value = telemetry.handBrake

        # Column 2, Suspension travel gauges
        susp_norm_fl.value = telemetry.suspensionTravelNormFL * 100
        susp_norm_fl.title = f"Front Left: {telemetry.suspensionTravelAbsFL}"
        susp_norm_fr.value = telemetry.suspensionTravelNormFR * 100
        susp_norm_fr.title = f"Front Right: {telemetry.suspensionTravelAbsFR}"
        susp_norm_rl.value = telemetry.suspensionTravelNormRL * 100
        susp_norm_rl.title = f"Rear Left: {telemetry.suspensionTravelAbsRL}"
        susp_norm_rr.value = telemetry.suspensionTravelNormRR * 100
        susp_norm_rr.title = f"Reaf Right: {telemetry.suspensionTravelAbsRR}"

        # For the final column, just output all the raw telemetry data along with lables
        raw.text = f"Idle RPM: {telemetry.idleRpm}\nAcceleration X: {telemetry.accelX}\nAcceleration Z: {telemetry.accelZ}\nVelocity X: {telemetry.velX}\nVelocity Z: {telemetry.velZ}\nAngular Velocity X: {telemetry.angularVelX}\nAngular Velocity Z: {telemetry.angularVelZ}\nTire Temp FL: {telemetry.tireTempFL}\nTire Temp FR: {telemetry.tireTempFR}\nTire Temp RL: {telemetry.tireTempRL}\nTire Temp RR: {telemetry.tireTempRR}\nSlip Ratio FL: {telemetry.tireSlipRatioFL}\nSlip Ratio FR: {telemetry.tireSlipRatioFR}\nSlip Ratio RL: {telemetry.tireSlipRatioRL}\nSlip Ratio RR: {telemetry.tireSlipRatioRR}\nTire Combined Slip FL: {telemetry.tireCombinedSlipFL}\nTire Combined Slip FR: {telemetry.tireCombinedSlipFR}\nTire Combined Slip RL: {telemetry.tireCombinedSlipRL}\nTire Combined Slip RR: {telemetry.tireCombinedSlipRR}\nWheel Rotation Speed FL: {telemetry.wheelRotationSpeedFL}\nWheel Rotation Speed FR: {telemetry.wheelRotationSpeedFR}\nWheel Rotation Speed RL: {telemetry.wheelRotationSpeedRL}\nWheel Rotation Speed RR: {telemetry.wheelRotationSpeedRR}\nSlip Angle FL: {telemetry.tireSlipAngleFL}\nSlip Angle FR: {telemetry.tireSlipAngleFR}\nSlip Angle RL: {telemetry.tireSlipAngleRL}\nSlip Angle RR: {telemetry.tireSlipAngleRR}\nRace On: {telemetry.raceOn}\nDistance Traveled: {telemetry.distanceTraveled}\nNorm Driving Line: {telemetry.normalizedDrivingLine}\nNorm AI Brake Diff: {telemetry.normalizedAIBrakeDifference}"

        ui.display()
