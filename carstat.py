class telemetry:

    # Constructor
    def __init__(self, returned_data):

        self.timestamp = returned_data["TimestampMS"]
        
        # Basic car metrics
        self.rpm            = int(returned_data["CurrentEngineRpm"])
        self.speed          = returned_data["Speed"]
        self.power          = returned_data["Power"]
        self.torque         = returned_data["Torque"]
        self.maxRpm         = returned_data["EngineMaxRpm"]
        self.idleRpm        = returned_data["EngineIdleRpm"]
        self.boost          = returned_data["Boost"]
        self.carClass       = returned_data["CarClass"]
        self.carPI          = returned_data["CarPerformanceIndex"]
        self.drivetrainType = returned_data["DrivetrainType"]
        self.numCylinders   = returned_data["NumCylinders"]

        # Control inputs
        self.accel      = returned_data["Accel"]
        self.brake      = returned_data["Brake"]
        self.steer      = returned_data["Steer"]
        self.gear       = returned_data["Gear"]
        self.handBrake  = returned_data["HandBrake"]
        self.clutch     = returned_data["Clutch"]

        # Absolute telemetry
        self.carOrdinal     = returned_data["CarOrdinal"]
        self.positionX      = returned_data["PositionX"]
        self.positionY      = returned_data["PositionY"]
        self.positionZ      = returned_data["PositionZ"]
        self.accelX         = returned_data["AccelerationX"]
        self.accelY         = returned_data["AccelerationY"]
        self.accelZ         = returned_data["AccelerationZ"]
        self.velX           = returned_data["VelocityX"]
        self.velY           = returned_data["VelocityY"]
        self.velZ           = returned_data["VelocityZ"]
        self.angularVelX    = returned_data["AngularVelocityX"]
        self.angularVelY    = returned_data["AngularVelocityY"]
        self.angularVelZ    = returned_data["AngularVelocityZ"]
        self.yaw            = returned_data["Yaw"]
        self.pitch          = returned_data["Pitch"]
        self.roll           = returned_data["Roll"]

        # Suspension
        self.suspensionTravelNormFL     = returned_data["NormalizedSuspensionTravelFrontLeft"]
        self.suspensionTravelNormFR     = returned_data["NormalizedSuspensionTravelFrontRight"]
        self.suspensionTravelNormRL     = returned_data["NormalizedSuspensionTravelRearLeft"]
        self.suspensionTravelNormRR     = returned_data["NormalizedSuspensionTravelRearRight"]
        self.suspensionTravelAbsFL      = returned_data["SuspensionTravelMetersFrontLeft"]
        self.suspensionTravelAbsFR      = returned_data["SuspensionTravelMetersFrontRight"]
        self.suspensionTravelAbsRL      = returned_data["SuspensionTravelMetersRearLeft"]
        self.suspensionTravelAbsRR      = returned_data["SuspensionTravelMetersRearRight"]

        # Tire
        self.tireTempFL             = returned_data["TireTempFrontLeft"]
        self.tireTempFR             = returned_data["TireTempFrontRight"]
        self.tireTempRL             = returned_data["TireTempRearLeft"]
        self.tireTempRR             = returned_data["TireTempRearRight"]
        self.tireSlipRatioFL        = returned_data["TireSlipRatioFrontLeft"]
        self.tireSlipRatioFR        = returned_data["TireSlipRatioFrontRight"]
        self.tireSlipRatioRL        = returned_data["TireSlipRatioRearLeft"]
        self.tireSlipRatioRR        = returned_data["TireSlipRatioRearRight"]
        self.tireSlipAngleFL        = returned_data["TireSlipAngleFrontLeft"]
        self.tireSlipAngleFR        = returned_data["TireSlipAngleFrontRight"]
        self.tireSlipAngleRL        = returned_data["TireSlipAngleRearLeft"]
        self.tireSlipAngleRR        = returned_data["TireSlipAngleRearRight"]
        self.tireCombinedSlipFL     = returned_data["TireCombinedSlipFrontLeft"]
        self.tireCombinedSlipFR     = returned_data["TireCombinedSlipFrontRight"]
        self.tireCombinedSlipRL     = returned_data["TireCombinedSlipRearLeft"]
        self.tireCombinedSlipRR     = returned_data["TireCombinedSlipRearRight"]
        self.wheelRotationSpeedFL   = returned_data["WheelRotationSpeedFrontLeft"]
        self.wheelRotationSpeedFR   = returned_data["WheelRotationSpeedFrontRight"]
        self.wheelRotationSpeedRL   = returned_data["WheelRotationSpeedRearLeft"]
        self.wheelRotationSpeedRR   = returned_data["WheelRotationSpeedRearRight"]
        
        # Simulation effects
        self.wheelOnRumbleStripFL = returned_data["WheelOnRumbleStripFrontLeft"]
        self.wheelOnRumbleStripFR = returned_data["WheelOnRumbleStripFrontRight"]
        self.wheelOnRumbleStripRL = returned_data["WheelOnRumbleStripRearLeft"]
        self.wheelOnRumbleStripRR = returned_data["WheelOnRumbleStripRearRight"]
        self.surfaceRumbleFL      = returned_data["SurfaceRumbleFrontLeft"]
        self.surfaceRumbleFR      = returned_data["SurfaceRumbleFrontRight"]
        self.surfaceRumbleRL      = returned_data["SurfaceRumbleRearLeft"]
        self.surfaceRumbleRR      = returned_data["SurfaceRumbleRearRight"]
        self.wheelInPuddleDepthFL = returned_data["WheelInPuddleDepthFrontLeft"]
        self.wheelInPuddleDepthFR = returned_data["WheelInPuddleDepthFrontRight"]
        self.wheelInPuddleDepthRL = returned_data["WheelInPuddleDepthRearLeft"]
        self.wheelInPuddleDepthRR = returned_data["WheelInPuddleDepthRearRight"]
        
        # Racing statistics
        self.raceOn             = returned_data["IsRaceOn"]
        self.distanceTraveled   = returned_data["DistanceTraveled"]
        self.bestLap            = returned_data["BestLap"]
        self.lastLap            = returned_data["LastLap"]
        self.currentLap         = returned_data["CurrentLap"]
        self.currentRaceTime    = returned_data["CurrentRaceTime"]
        self.lapNumber          = returned_data["LapNumber"]
        self.racePosition       = returned_data["RacePosition"]
        self.normalizedDrivingLine          = returned_data["NormalizedDrivingLine"]
        self.normalizedAIBrakeDifference    = returned_data["NormalizedAIBrakeDifference"]
