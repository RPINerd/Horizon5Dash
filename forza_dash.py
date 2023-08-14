# Forza Dash
# A simple app for Forza Horizon 5 that can recieve the in-game telemetry
# and display it in real time in a customizable dashboard.
#

import json
import socket
import sys

import carstat


def get_data(data):
    return_dict = {}

    # Additional var
    passed_data = data

    # For each data type, get size and then collect
    for key in data_types:
        d_type = data_types[key]
        size = byte_skus[d_type]
        current = passed_data[:size]

        decoded = 0
        # Decoding for each type of data
        if d_type == "s32":
            decoded = int.from_bytes(current, byteorder="little", signed=True)
        elif d_type == "u32":
            decoded = int.from_bytes(current, byteorder="little", signed=False)
        elif d_type == "f32":
            decoded = struct.unpack("f", current)[0]
        elif d_type == "u16":
            decoded = struct.unpack("H", current)[0]
        elif d_type == "u8":
            decoded = struct.unpack("B", current)[0]
        elif d_type == "s8":
            decoded = struct.unpack("b", current)[0]

        # Add decoded data to the dict
        return_dict[key] = decoded

        # Remove the already read bytes from the variable
        passed_data = passed_data[size:]

    return return_dict


def open_socket(server_address, port) -> socket.socket:
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    sock.bind(server_address)

    return sock


def main():
    # Read in data types from file
    data_types = {}
    with open("data_formats.txt", "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            data_types[line.split()[1]] = line.split()[0]

    # Establish connection to the telemetry output
    sock = open_socket("localhost", 10000)

    # Primary loop
    while True:
        # Recieve incoming data
        data, address = sock.recvfrom(1500)

        # Convert recieved data to a dictionary
        returned_data = get_data(data)

        # Transfer select data to variables
        currentEngineRpm = returned_data["CurrentEngineRpm"]
        accelerationX = returned_data["AccelerationX"]
        accelerationY = returned_data["AccelerationY"]
        accelerationZ = returned_data["AccelerationZ"]
        velocityX = returned_data["VelocityX"]
        velocityY = returned_data["VelocityY"]
        velocityZ = returned_data["VelocityZ"]
        yaw = returned_data["Yaw"]
        pitch = returned_data["Pitch"]
        roll = returned_data["Roll"]
        normalizedSuspensionTravelFL = returned_data[
            "NormalizedSuspensionTravelFrontLeft"
        ]
        normalizedSuspensionTravelFR = returned_data[
            "NormalizedSuspensionTravelFrontRight"
        ]
        normalizedSuspensionTravelRL = returned_data[
            "NormalizedSuspensionTravelRearLeft"
        ]
        normalizedSuspensionTravelRR = returned_data[
            "NormalizedSuspensionTravelRearRight"
        ]
        tireSlipRatioFrontLeft = returned_data["TireSlipRatioFrontLeft"]
        tireSlipRatioFrontRight = returned_data["TireSlipRatioFrontRight"]
        tireSlipRatioRearLeft = returned_data["TireSlipRatioRearLeft"]
        tireSlipRatioRearRight = returned_data["TireSlipRatioRearRight"]
        tireSlipAngleFrontLeft = returned_data["TireSlipAngleFrontLeft"]
        tireSlipAngleFrontRight = returned_data["TireSlipAngleFrontRight"]
        tireSlipAngleRearLeft = returned_data["TireSlipAngleRearLeft"]
        tireSlipAngleRearRight = returned_data["TireSlipAngleRearRight"]
        tireCombinedSlipFrontLeft = returned_data["TireCombinedSlipFrontLeft"]
        tireCombinedSlipFrontRight = returned_data["TireCombinedSlipFrontRight"]
        tireCombinedSlipRearLeft = returned_data["TireCombinedSlipRearLeft"]
        tireCombinedSlipRearRight = returned_data["TireCombinedSlipRearRight"]
        suspensionTravelMetersFrontLeft = returned_data[
            "SuspensionTravelMetersFrontLeft"
        ]
        suspensionTravelMetersFrontRight = returned_data[
            "SuspensionTravelMetersFrontRight"
        ]
        suspensionTravelMetersRearLeft = returned_data["SuspensionTravelMetersRearLeft"]
        suspensionTravelMetersRearRight = returned_data[
            "SuspensionTravelMetersRearRight"
        ]
        speed = returned_data["Speed"]
        power = returned_data["Power"]
        torque = returned_data["Torque"]
        tireTempFrontLeft = returned_data["TireTempFrontLeft"]
        tireTempFrontRight = returned_data["TireTempFrontRight"]
        tireTempRearLeft = returned_data["TireTempRearLeft"]
        tireTempRearRight = returned_data["TireTempRearRight"]
        boost = returned_data["Boost"]
        accel = returned_data["Accel"]
        brake = returned_data["Brake"]
        clutch = returned_data["Clutch"]
        handBrake = returned_data["HandBrake"]
        gear = returned_data["Gear"]
        steer = returned_data["Steer"]

        # Unused data (for now)
        # raceOn = returned_data["IsRaceOn"]
        # timestamp = returned_data["TimestampMS"]
        # engineMaxRpm = returned_data["EngineMaxRpm"]
        # engineIdleRpm = returned_data["EngineIdleRpm"]
        # angularVelocityX = returned_data["AngularVelocityX"]
        # angularVelocityY = returned_data["AngularVelocityY"]
        # angularVelocityZ = returned_data["AngularVelocityZ"]
        # wheelRotationSpeedFrontLeft = returned_data["WheelRotationSpeedFrontLeft"]
        # wheelRotationSpeedFrontRight = returned_data["WheelRotationSpeedFrontRight"]
        # wheelRotationSpeedRearLeft = returned_data["WheelRotationSpeedRearLeft"]
        # wheelRotationSpeedRearRight = returned_data["WheelRotationSpeedRearRight"]
        # wheelOnRumbleStripFrontLeft = returned_data["WheelOnRumbleStripFrontLeft"]
        # wheelOnRumbleStripFrontRight = returned_data["WheelOnRumbleStripFrontRight"]
        # wheelOnRumbleStripRearLeft = returned_data["WheelOnRumbleStripRearLeft"]
        # wheelOnRumbleStripRearRight = returned_data["WheelOnRumbleStripRearRight"]
        # wheelInPuddleDepthFrontLeft = returned_data["WheelInPuddleDepthFrontLeft"]
        # wheelInPuddleDepthFrontRight = returned_data["WheelInPuddleDepthFrontRight"]
        # wheelInPuddleDepthRearLeft = returned_data["WheelInPuddleDepthRearLeft"]
        # wheelInPuddleDepthRearRight = returned_data["WheelInPuddleDepthRearRight"]
        # surfaceRumbleFrontLeft = returned_data["SurfaceRumbleFrontLeft"]
        # surfaceRumbleFrontRight = returned_data["SurfaceRumbleFrontRight"]
        # surfaceRumbleRearLeft = returned_data["SurfaceRumbleRearLeft"]
        # surfaceRumbleRearRight = returned_data["SurfaceRumbleRearRight"]
        # carOrdinal = returned_data["CarOrdinal"]
        # carClass = returned_data["CarClass"]
        # carPerformanceIndex = returned_data["CarPerformanceIndex"]
        # drivetrainType = returned_data["DrivetrainType"]
        # numCylinders = returned_data["NumCylinders"]
        # positionX = returned_data["PositionX"]
        # positionY = returned_data["PositionY"]
        # positionZ = returned_data["PositionZ"]
        # distanceTraveled = returned_data["DistanceTraveled"]
        # bestLap = returned_data["BestLap"]
        # lastLap = returned_data["LastLap"]
        # currentLap = returned_data["CurrentLap"]
        # currentRaceTime = returned_data["CurrentRaceTime"]
        # lapNumber = returned_data["LapNumber"]
        # racePosition = returned_data["RacePosition"]
        # normalizedDrivingLine = returned_data["NormalizedDrivingLine"]
        # normalizedAIBrakeDifference = returned_data["NormalizedAIBrakeDifference"]
