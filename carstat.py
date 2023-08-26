class telemetry:
    # Constructor
    def __init__(self, returned_data):
        self.timestamp = returned_data["TimestampMS"]

        # Basic car metrics
        self.idleRpm = int(returned_data["EngineIdleRpm"])
        self.rpm = returned_data["CurrentEngineRpm"]
        self.maxRpm = int(returned_data["EngineMaxRpm"])
        self.speed = (1 / 0.44704) * returned_data["Speed"]  # Convert from m/s to mph
        self.power = (
            0 if returned_data["Power"] < 0 else int(returned_data["Power"] / 745.69987)
        )  # Convert watts to horsepower
        self.torque = (
            0 if returned_data["Torque"] < 0 else int(returned_data["Torque"] / 1.35582)
        )  # Convert Nm to lb-ft
        self.boost = 0 if returned_data["Boost"] < 1 else round(returned_data["Boost"], 1)
        self.carPI = returned_data["CarPerformanceIndex"]
        match returned_data["CarClass"]:
            case 0:
                self.carClass = "D"
            case 1:
                self.carClass = "C"
            case 2:
                self.carClass = "B"
            case 3:
                self.carClass = "A"
            case 4:
                self.carClass = "S1"
            case 5:
                self.carClass = "S2"
            case 6:
                self.carClass = "X"
            case _:
                raise f"Unknown car class {returned_data['CarClass']}!"
        match returned_data["DrivetrainType"]:
            case 0:
                self.drivetrainType = "FWD"
            case 1:
                self.drivetrainType = "RWD"
            case 2:
                self.drivetrainType = "AWD"
            case _:
                raise f"Unknown drivetrain type {returned_data['DrivetrainType']}!"
        self.numCylinders = returned_data["NumCylinders"]

        # Control inputs
        self.accel = (1 / 255) * returned_data["Accel"] * 100
        self.brake = (1 / 255) * returned_data["Brake"] * 100
        self.steer = returned_data["Steer"]
        self.gear = returned_data["Gear"]
        self.handBrake = returned_data["HandBrake"] / 255
        self.clutch = (1 / 255) * returned_data["Clutch"] * 100

        # Absolute telemetry
        self.carOrdinal = returned_data["CarOrdinal"]
        self.positionX = round(returned_data["PositionX"], 6)
        self.positionY = round(returned_data["PositionY"], 6)
        self.positionZ = round(returned_data["PositionZ"], 6)
        self.accelX = round(returned_data["AccelerationX"], 6)
        # self.accelY = round(returned_data["AccelerationY"], 6)
        self.accelZ = round(returned_data["AccelerationZ"], 6)
        self.velX = round(returned_data["VelocityX"], 6)
        # self.velY = returned_data["VelocityY"], 6)
        self.velZ = round(returned_data["VelocityZ"], 6)
        self.angularVelX = round(returned_data["AngularVelocityX"], 6)
        # self.angularVelY = returned_data["AngularVelocityY"], 6)
        self.angularVelZ = round(returned_data["AngularVelocityZ"], 6)
        self.yaw = round(returned_data["Yaw"], 6)
        self.pitch = round(returned_data["Pitch"], 6)
        self.roll = round(returned_data["Roll"], 6)

        # Suspension
        self.suspensionTravelNormFL = round(returned_data["NormalizedSuspensionTravelFrontLeft"], 6)
        self.suspensionTravelNormFR = round(returned_data["NormalizedSuspensionTravelFrontRight"], 6)
        self.suspensionTravelNormRL = round(returned_data["NormalizedSuspensionTravelRearLeft"], 6)
        self.suspensionTravelNormRR = round(returned_data["NormalizedSuspensionTravelRearRight"], 6)
        self.suspensionTravelAbsFL = round(returned_data["SuspensionTravelMetersFrontLeft"], 6)
        self.suspensionTravelAbsFR = round(returned_data["SuspensionTravelMetersFrontRight"], 6)
        self.suspensionTravelAbsRL = round(returned_data["SuspensionTravelMetersRearLeft"], 6)
        self.suspensionTravelAbsRR = round(returned_data["SuspensionTravelMetersRearRight"], 6)

        # Tire
        self.tireTempFL = round(returned_data["TireTempFrontLeft"], 2)
        self.tireTempFR = round(returned_data["TireTempFrontRight"], 2)
        self.tireTempRL = round(returned_data["TireTempRearLeft"], 2)
        self.tireTempRR = round(returned_data["TireTempRearRight"], 2)
        self.tireSlipRatioFL = abs(int(returned_data["TireSlipRatioFrontLeft"] * 100))
        self.tireSlipRatioFR = abs(int(returned_data["TireSlipRatioFrontRight"] * 100))
        self.tireSlipRatioRL = abs(int(returned_data["TireSlipRatioRearLeft"] * 100))
        self.tireSlipRatioRR = abs(int(returned_data["TireSlipRatioRearRight"] * 100))
        self.tireSlipAngleFL = round(returned_data["TireSlipAngleFrontLeft"], 6)
        self.tireSlipAngleFR = round(returned_data["TireSlipAngleFrontRight"], 6)
        self.tireSlipAngleRL = round(returned_data["TireSlipAngleRearLeft"], 6)
        self.tireSlipAngleRR = round(returned_data["TireSlipAngleRearRight"], 6)
        self.tireCombinedSlipFL = round(returned_data["TireCombinedSlipFrontLeft"], 6)
        self.tireCombinedSlipFR = round(returned_data["TireCombinedSlipFrontRight"], 6)
        self.tireCombinedSlipRL = round(returned_data["TireCombinedSlipRearLeft"], 6)
        self.tireCombinedSlipRR = round(returned_data["TireCombinedSlipRearRight"], 6)
        self.wheelRotationSpeedFL = round(returned_data["WheelRotationSpeedFrontLeft"], 3)
        self.wheelRotationSpeedFR = round(returned_data["WheelRotationSpeedFrontRight"], 3)
        self.wheelRotationSpeedRL = round(returned_data["WheelRotationSpeedRearLeft"], 3)
        self.wheelRotationSpeedRR = round(returned_data["WheelRotationSpeedRearRight"], 3)

        # Simulation effects
        # self.wheelOnRumbleStripFL = returned_data["WheelOnRumbleStripFrontLeft"]
        # self.wheelOnRumbleStripFR = returned_data["WheelOnRumbleStripFrontRight"]
        # self.wheelOnRumbleStripRL = returned_data["WheelOnRumbleStripRearLeft"]
        # self.wheelOnRumbleStripRR = returned_data["WheelOnRumbleStripRearRight"]
        # self.surfaceRumbleFL = returned_data["SurfaceRumbleFrontLeft"]
        # self.surfaceRumbleFR = returned_data["SurfaceRumbleFrontRight"]
        # self.surfaceRumbleRL = returned_data["SurfaceRumbleRearLeft"]
        # self.surfaceRumbleRR = returned_data["SurfaceRumbleRearRight"]
        # self.wheelInPuddleDepthFL = returned_data["WheelInPuddleDepthFrontLeft"]
        # self.wheelInPuddleDepthFR = returned_data["WheelInPuddleDepthFrontRight"]
        # self.wheelInPuddleDepthRL = returned_data["WheelInPuddleDepthRearLeft"]
        # self.wheelInPuddleDepthRR = returned_data["WheelInPuddleDepthRearRight"]

        # Racing statistics
        self.raceOn = returned_data["IsRaceOn"]
        self.distanceTraveled = returned_data["DistanceTraveled"]
        self.bestLap = returned_data["BestLap"]
        self.lastLap = returned_data["LastLap"]
        self.currentLap = returned_data["CurrentLap"]
        self.currentRaceTime = returned_data["CurrentRaceTime"]
        self.lapNumber = returned_data["LapNumber"]
        self.racePosition = returned_data["RacePosition"]
        self.normalizedDrivingLine = returned_data["NormalizedDrivingLine"]
        self.normalizedAIBrakeDifference = returned_data["NormalizedAIBrakeDifference"]

    def normalized_rpm(self):
        if self.maxRpm == 0:
            return 0
        else:
            return int(self.rpm / (self.maxRpm - self.idleRpm) * 100)
