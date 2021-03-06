# By DankMeme_Master101, Alex Rowell, with help from 2015 robot.py by Alex Rowell, Beniamino Briganti, Lucca Buonamano, Blake Mountford and Lex Martin
import wpilib
from networktables import NetworkTables
import math
import rigs.controlstemplate as controlstemplate
from enum import Enum

JOYSTICK_PORT = 0
LEFT_MOTOR = 1
RIGHT_MOTOR = 3
WINCH_MOTOR = 4
distOneSecond = 2
class TupperBot(wpilib.IterativeRobot):
    def robotInit(self):

        self.pegChooser = wpilib.SendableChooser()
        self.pegChooser.addObject('Left', 'left')
        self.pegChooser.addObject('Right', 'right')
        self.pegChooser.addObject('Middle', 'middle')
        wpilib.SmartDashboard.putData('ChooseYourPeg', self.pegChooser)
        #test = sd.getNumber("someNumber")
        #self.logger.info("Test = " + str(test))
        self.logger.info("Robot Starting up...")
        self.logger.info("Camera started")
        self.mctype = wpilib.Spark
        self.logger.info("Defined motor controller type")
        self.cam_horizontal = wpilib.Servo(6)
        self.cam_vertical = wpilib.Servo(7)
        self.cam_vertical_value = 0.2
        self.cam_horizontal_value = 0.5
        self.logger.info("Defined Camera Servos and Respective Values")
        self.cam_horizontal.set(self.cam_horizontal_value)
        self.cam_vertical.set(self.cam_vertical_value)
        self.logger.info("Set Camera Servos to Halfway")
        self.pdp = wpilib.PowerDistributionPanel()
        self.logger.info("defined PowerDistributionPanel")
        self.left = self.mctype(LEFT_MOTOR)
        self.right = self.mctype(RIGHT_MOTOR)
        self.winchMotor = self.mctype(WINCH_MOTOR)
        self.logger.info("Defined FL, BL, FR, BR motors")
        self.controls = controlstemplate.Controls(wpilib.Joystick(JOYSTICK_PORT), self.isTest)
        self.logger.info("Defined Control scheme")
        self.timer = wpilib.Timer()
        self.logger.info("Defined Timer")
        self.logger.info("Robot On")
    def disabledInit(self):
        self.logger.info('Disabled mode')

    def testInit(self):
        self.logger.info('Test mode')

    def autonomousInit(self):
        self.logger.info("Autonomous Mode")
        self.pegDriveState = "start"
        self.peg = self.pegChooser.getSelected()

        # resets and starts the timer at the beginning of autonomous
        self.timer.reset()
        self.timer.start()

    def calculate_drive(self, forward, turn):
        #left_value = -forward + turn
        #left_value *= math.fabs(left_value)
        #multiplier = self.controls.get_throttle_multiplier()
        #left_value *= multiplier
        #right_value = -forward - turn
        #right_value *= math.fabs(right_value)
        #right_value *= multiplier

        left_value = turn + forward * -1
        right_value = turn + forward


        return left_value, right_value  # TODO invert the right side at the controller config level

    def arcade_drive(self, forward, turn):
        left_value, right_value = self.calculate_drive(forward, turn)
        # in test mode, if the motor toggle for a wheel is disabled, we keep it set to 0
        self.left.set(left_value if self.controls.lf_toggle or not self.isTest() else 0)
        self.right.set(right_value if self.controls.rf_toggle or not self.isTest() else 0)

    def autonomous_middle_peg(self):
        distToPeg = 1.8288
        if self.timer.get() < distToPeg / distOneSecond:
            self.arcade_drive(1, 0)
        else:
            self.arcade_drive(0, 0)


    def autonomous_turn(self):

        if self.peg == "right":
            turnValue = 1
        else:
            turnValue = -1
        distPastAirship = 1
        distIntoAirship = 1
        timeToTurn = 1
        if self.pegDriveState == "forwardPastAirship":
            if self.timer.get() < distPastAirship / distOneSecond:
                self.arcade_drive(1, 0)
            else:
                self.arcade_drive(0, 0)
                self.pegDriveState = "turn"
                self.timer.reset()
        if self.pegDriveState == "turn":
            if (self.timer.get() < timeToTurn):
                self.arcade_drive(0, turnValue)
            else:
                self.arcade_drive(0, 0)
                self.timer.reset()
        if self.pegDriveState == 'forwardIntoAirship':
            if self.timer.get() < distIntoAirship / distOneSecond:
                self.arcade_drive(1, 0)
            else:
                self.arcade_drive(0, 0)






    def autonomousPeriodic(self):
        if (self.peg == "middle"):
            self.autonomous_middle_peg()
        elif (self.peg=="right" or self.peg=="left"):
            self.autonomous_turn()


    def teleopInit(self):
        self.logger.info("Teleoperated Mode")

    def winchActivate(self, speed):
        self.winchMotor.setSpeed(speed)





    def teleopPeriodic(self):
        self.controls.update()
        self.arcade_drive(self.controls.forward(), (self.controls.turn()))
        if self.controls.reset_cam():
            self.cam_horizontal_value = 0.5
            self.cam_vertical_value = 0.1
        if self.controls.debug_button():
            self.print_debug_info()
        if self.controls.climb_up():
            self.winchMotor.set(1)
        elif self.controls.climb_down():
            self.winchMotor.set(-1)
        else:
            self.winchActivate(0)
        if self.controls.move_cam_up():
            self.cam_vertical_value -= 0.001
        elif self.controls.move_cam_down():
            self.cam_vertical_value += 0.001
        elif self.controls.move_cam_left():
            self.cam_horizontal_value += 0.001
        elif self.controls.move_cam_right():
            self.cam_horizontal_value -= 0.001
        self.cam_horizontal.set(self.cam_horizontal_value)
        self.cam_vertical.set(self.cam_vertical_value)


       # try:
       #     self.camera
       #     exp = self.camera.exposureValue
       #     if self.controls.exposure_up_button() and exp < 100:
       #         self.camera.setExposureManual(exp + 10)
       #     if self.controls.exposure_down_button() and exp > 0:
       #         self.camera.setExposureManual(exp - 10)
       # except AttributeError:
       #     print("")

    def disabledPeriodic(self):
        self.right.set(0)
        self.left.set(0)

    def print_debug_info(self):
        self.logger.info("debug info here")
        try:
            # only if camera is configured
            self.camera
            self.logger.info("camera active: " + str(self.camera.active))
            self.logger.info("camera name: " + str(self.camera.name))
            self.logger.info("camera exposure: " + str(self.camera.exposureValue))
            self.logger.info("camera fps: " + str(self.camera.fps))
            self.logger.info("camera res: " + str(self.camera.width) + "x" + str(self.camera.height))

        except AttributeError:
            pass

    def testPeriodic(self):
        self.teleopPeriodic()

if __name__ == '__main__':
    wpilib.run(TupperBot)
