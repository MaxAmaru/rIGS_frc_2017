#By Alex Rowell, Beniamino Briganti, Lucca Buonamano, Blake Mountford and Lex Martin. Rewritten by Max Scurrah-Rose and Alex Rowell

import logging
import math

import wpilib


class ControlsTemplate:

    def get_throttle_multiplier(self):
        print("override me")

    def message_test(self):
        print("override me")

    def debug_button(self):
        print("override me")

    def exposure_up_button(self):
        print("override me")

    def exposure_down_button(self):
        print("override me")

    def forward(self):
        print("override me")

    def turn(self):
        print("override me")

    def lift_portcullis(self):
        print("override me")

    def lower_portcullis(self):
        print("override me")



class Controls(ControlsTemplate):

    # Joystick Buttons
    DEBUG_BUTTON = 7
    #EXPOSURE_UP_BUTTON = 12
    #EXPOSURE_DOWN_BUTTON = 11
    TRIGGER = 1
    THUMB_BUTTON = 2
    TOGGLE_DRIVE_BUTTON = 3
    MOVE_CAMERA_LEFT = 9
    MOVE_CAMERA_RIGHT = 10
    MOVE_CAMERA_UP = 8
    MOVE_CAMERA_DOWN = 12
    logger = logging.getLogger('old_controls')


    def __init__(self, joystick, is_test):
        self.isTest = is_test
        self.stick = joystick
        self.multiplier = 1
        # motors can be disabled with these:
        self.lf_toggle = True
        self.toggle_listen = 0.0
        self.lb_toggle = True
        self.rf_toggle = True
        self.rb_toggle = True
        self.logger.debug("old controls constructor")
        self.timer = wpilib.Timer()
        self.timer.reset()
        self.timer.start()

    def get_throttle_multiplier(self):
        new_multiplier = (-self.stick.getThrottle() + 1) / 2
        diff = math.fabs(new_multiplier - self.multiplier)
        if diff > 0.1:
            self.logger.info("Throttle: " + str(new_multiplier))
            wpilib.SmartDashboard.putString('throttle', str(new_multiplier))
        self.multiplier = new_multiplier
        return self.multiplier

    def debug_button(self):
        return self.stick.getRawButton(self.DEBUG_BUTTON)

    def get_camera_position(self):
        return self.stick.getX()

    #def exposure_up_button(self):
    #   return self.stick.getRawButton(self.EXPOSURE_UP_BUTTON)

    #def exposure_down_button(self):
    #    return self.stick.getRawButton(self.EXPOSURE_DOWN_BUTTON)

    #def message_test(self):
    #    return self.stick.getRawButton(self.MESSAGE_TEST)

    def forward(self):
        return -self.stick.getY()

    def turn(self):
        return self.stick.getZ()
    def move_cam_up(self):
        return self.stick.getRawButton(self.MOVE_CAMERA_UP)
    def move_cam_down(self):
        return self.stick.getRawButton(self.MOVE_CAMERA_DOWN)
    def reset_cam(self):
        return self.stick.getRawButton(11)
    def test(self):
        return 1
    def move_cam_left(self):
        return self.stick.getRawButton(self.MOVE_CAMERA_LEFT)
    def move_cam_right(self):
        return self.stick.getRawButton(self.MOVE_CAMERA_RIGHT)
    def climb_up(self):
        return self.stick.getRawButton(self.TRIGGER)
    def climb_down(self):
        return self.stick.getRawButton(self.THUMB_BUTTON)
    def update(self):
        if self.isTest():
            self.logger.info("Test Mode Not Implemented!")


# TODO ps3 controls, keyboard controls and alternate joystick controls
class NewControls(ControlsTemplate):

    MESSAGE_TEST = 4
    DEBUG_BUTTON = 7
    EXPOSURE_UP_BUTTON = 5
    EXPOSURE_DOWN_BUTTON = 6

    logger = logging.getLogger('new_controls')

    def __init__(self, joystick, is_test):
        self.stick = joystick
        self.isTest = is_test
        self.multiplier = 1
        self.throttle_toggle = False

    def get_throttle_multiplier(self):
        new_multiplier = (-self.stick.getThrottle() + 1) / 2
        if math.fabs(new_multiplier - self.multiplier) > 0.1:
            wpilib.SmartDashboard.putString('/SmartDashboard/throttle', str(new_multiplier))
        self.multiplier = new_multiplier
        return self.multiplier

    def debug_button(self):
        return self.stick.getRawButton(self.DEBUG_BUTTON)

    def exposure_up_button(self):
        return self.stick.getRawButton(self.EXPOSURE_UP_BUTTON)

    def exposure_down_button(self):
        return self.stick.getRawButton(self.EXPOSURE_DOWN_BUTTON)

    def message_test(self):
        return self.stick.getRawButton(self.MESSAGE_TEST)

    def forward(self):
        return self.stick.getY()

    def turn(self):
        return self.stick.getX()
    def turn_camera(self):
        return