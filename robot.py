# By DankMeme_Master101, Alex Rowell, with help from 2015 robot.py by Alex Rowell, Beniamino Briganti, Lucca Buonamano, Blake Mountford and Lex Martin
import wpilib
#from networktables import NetworkTables
import math
import rigs.controlstemplate

JOYSTICK_PORT = 0
BACK_RIGHT = 0
FRONT_RIGHT = 1
BACK_LEFT = 2
FRONT_LEFT = 3
WINCH_MOTOR = 4

class TupperBot(wpilib.IterativeRobot):
    def robotInit(self):
        #NetworkTables.initialize(server='roborio-5893-frc.local')
        #sd = NetworkTables.getTable('SmartDashboard')
        #sd.putNumber('someNumber', 1234)
        #test = sd.getNumber("someNumber")
        #self.logger.info("Test = " + str(test))
        self.logger.info("Robot Starting up...")
        self.mctype = wpilib.Spark
        self.logger.info("Defined motor controller type")
        self.pdp = wpilib.PowerDistributionPanel()
        self.logger.info("defined PowerDistributionPanel")
        self.leftFront = self.mctype(FRONT_LEFT)
        self.leftBack = self.mctype(BACK_LEFT)
        self.rightFront = self.mctype(FRONT_RIGHT)
        self.rightBack = self.mctype(BACK_RIGHT)
        self.winchMotor = wpilib.TalonSRX(WINCH_MOTOR)
        self.logger.info("Defined FL, BL, FR, BR motors")
        self.controls = rigs.controlstemplate.Controls(wpilib.Joystick(JOYSTICK_PORT), self.isTest)
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
        # resets and starts the timer at the beginning of autonomous
        self.timer.reset()
        self.timer.start()

    def calculate_drive(self, forward, turn):
        left_value = -forward + turn
        left_value *= math.fabs(left_value)
        multiplier = self.controls.get_throttle_multiplier()
        left_value *= multiplier
        right_value = -forward - turn
        right_value *= math.fabs(right_value)
        right_value *= multiplier
        return left_value, -right_value  # TODO invert the right side at the controller config level

    def arcade_drive(self, forward, turn):
        left_value, right_value = self.calculate_drive(forward, turn)

        # in test mode, if the motor toggle for a wheel is disabled, we keep it set to 0
        self.leftFront.set(left_value if self.controls.lf_toggle or not self.isTest() else 0)
        self.leftBack.set(left_value if self.controls.lb_toggle or not self.isTest() else 0)
        self.rightFront.set(right_value if self.controls.rf_toggle or not self.isTest() else 0)
        self.rightBack.set(right_value if self.controls.rb_toggle or not self.isTest() else 0)

    def autonomousPeriodic(self):
        self.logger.info("Autonomous Mode not implemented")

    def teleopInit(self):
        self.logger.info("Teleoperated Mode")

    def winchActivate(self, speed):
        self.winchMotor.setSpeed(speed)





    def teleopPeriodic(self):
        self.controls.update()
        self.arcade_drive(self.controls.forward(), (self.controls.turn()))

        if self.controls.debug_button():
            self.print_debug_info()

        if self.controls.climb_up():
            self.winchActivate(1)
        elif self.controls.climb_down():
            self.winchActivate(-1)
        else:
            self.winchActivate(0)

        try:
            self.camera
            exp = self.camera.exposureValue
            if self.controls.exposure_up_button() and exp < 100:
                self.camera.setExposureManual(exp + 10)
            if self.controls.exposure_down_button() and exp > 0:
                self.camera.setExposureManual(exp - 10)
        except AttributeError:
            pass

    def disabledPeriodic(self):
        self.leftFront.set(0)
        self.leftBack.set(0)
        self.rightFront.set(0)
        self.rightBack.set(0)

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
