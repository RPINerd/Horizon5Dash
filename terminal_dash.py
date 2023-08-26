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
    # Barebones output for now
    # print("Speed | RPM | Gear")

    column0 = VSplit(
        # RPM Gauge along the height of the left-most column
        ColorRangeVGauge(
            title="RPM: 100",
            val=0,
            border_color=2,
            colormap=(
                (70, 2),
                (85, 3),
                (95, 1),
            ),
        ),
    )

    column1 = VSplit(
        Text("", title="Car Info", color=1),
        # Horizontal gauges along the bottom, summarizing control inputs
        HSplit(
            # Current speed and acceleration pedal position
            VGauge(title="Speed", val=0, border_color=2, color=1),
            # Brake pedal position
            VGauge(title="Brake", val=0, border_color=2, color=1),
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
    rpm = ui.items[0].items[0]
    info = ui.items[1].items[0]
    speed = ui.items[1].items[1].items[0]
    brake = ui.items[1].items[1].items[1]
    susp_norm_fl = ui.items[2].items[0].items[0]
    susp_norm_fR = ui.items[2].items[0].items[1]
    susp_norm_rl = ui.items[2].items[1].items[0]
    susp_norm_rr = ui.items[2].items[1].items[1]
    raw = ui.items[3].items[0]

    # Sliding window for telemetry data
    telemetry_window = []

    while True:
        # Get the data from the socket
        telemetry_window = utils.recieve_telemetry(sock, data_types, telemetry_window, args.window)

        # Get the most recent telemetry data
        telemetry = telemetry_window[-1]

        info.text = f"Class: {telemetry.carClass}\nPI: {telemetry.carPI}\nDrivetrain: \
            {telemetry.drivetrainType}\nCylinders: {telemetry.numCylinders}\n \
            Gear: {telemetry.gear}\nPower: {telemetry.power}\nTorque: {telemetry.torque}\n \
            Boost: {telemetry.boost}"

        speed.title = f"Speed: {int(telemetry.speed)} mph {telemetry.suspensionTravelNormFL}"
        speed.value = telemetry.accel
        brake.value = telemetry.brake
        rpm.title = f"RPM   {int(telemetry.rpm)}"
        rpm.value = telemetry.normalized_rpm()
        susp_norm_fl.value = telemetry.suspensionTravelNormFL * 100
        susp_norm_fR.value = telemetry.suspensionTravelNormFR * 100
        susp_norm_rl.value = telemetry.suspensionTravelNormRL * 100
        susp_norm_rr.value = telemetry.suspensionTravelNormRR * 100

        # For the final column, just output all the raw telemetry data along with lables
        raw.text = f"Idle RPM: {telemetry.idleRpm}\nHandbrake: {telemetry.handBrake}\nClutch: {telemetry.clutch}\nCar Ordinal: {telemetry.carOrdinal}\nPosition X: {telemetry.positionX}\nPosition Y: {telemetry.positionY}\nPosition Z: {telemetry.positionZ}\nAcceleration X: {telemetry.accelX}\nAcceleration Z: {telemetry.accelZ}\nVelocity X: {telemetry.velX}\nVelocity Z: {telemetry.velZ}\nAngular Velocity X: {telemetry.angularVelX}\nAngular Velocity Z: {telemetry.angularVelZ}\nYaw: {telemetry.yaw}\nPitch: {telemetry.pitch}\nRoll: {telemetry.roll}\nAbsolute Suspension Travel FL: {telemetry.suspensionTravelAbsFL}\nAbsolute Suspension Travel FR: {telemetry.suspensionTravelAbsFR}\nAbsolute Suspension Travel RL: {telemetry.suspensionTravelAbsRL}\nAbsolute Suspension Travel RR: {telemetry.suspensionTravelAbsRR}\nTire Temp FL: {telemetry.tireTempFL}\nTire Temp FR: {telemetry.tireTempFR}\nTire Temp RL: {telemetry.tireTempRL}\nTire Temp RR: {telemetry.tireTempRR}\nSlip Ratio FL: {telemetry.tireSlipRatioFL}\nSlip Ratio FR: {telemetry.tireSlipRatioFR}\nSlip Ratio RL: {telemetry.tireSlipRatioRL}\nSlip Ratio RR: {telemetry.tireSlipRatioRR}\nTire Combined Slip FL: {telemetry.tireCombinedSlipFL}\nTire Combined Slip FR: {telemetry.tireCombinedSlipFR}\nTire Combined Slip RL: {telemetry.tireCombinedSlipRL}\nTire Combined Slip RR: {telemetry.tireCombinedSlipRR}\nWheel Rotation Speed FL: {telemetry.wheelRotationSpeedFL}\nWheel Rotation Speed FR: {telemetry.wheelRotationSpeedFR}\nWheel Rotation Speed RL: {telemetry.wheelRotationSpeedRL}\nWheel Rotation Speed RR: {telemetry.wheelRotationSpeedRR}\nSlip Angle FL: {telemetry.tireSlipAngleFL}\nSlip Angle FR: {telemetry.tireSlipAngleFR}\nSlip Angle RL: {telemetry.tireSlipAngleRL}\nSlip Angle RR: {telemetry.tireSlipAngleRR}\nRace On: {telemetry.raceOn}\nDistance Traveled: {telemetry.distanceTraveled}\nNorm Driving Line: {telemetry.normalizedDrivingLine}\nNorm AI Brake Diff: {telemetry.normalizedAIBrakeDifference}"

        ui.display()
