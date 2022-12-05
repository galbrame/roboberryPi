#!/bin/python3

#-----------------------------------------
# REMARKS: Some reuseable constants and code for the Python scripts.
#
#-----------------------------------------

import RPi.GPIO as GPIO


#-----------CONSTANTS-----------

# gpio pins for wheel directions
LEFT_FWD = 5
LEFT_REV = 6
RIGHT_FWD = 13
RIGHT_REV = 19

# gpio for pulse width modulation power/speed control
PWM = 18

# gpio for the LED
LED = 10


#----------FUNCTIONS----------

#------------------------------------------
# gpioSetup
#
# DESCRIPTION: Sets all the gpios for use
#
#-----------------------------------------
def gpioSetup():
    GPIO.setmode(GPIO.BCM)

    # Setting warnings to False instead of using RPi.cleanup() because
    # I don't want to reset the pins to INPUT before the shell scripts
    # but I still need to call setup() each time I run .py scripts.
    GPIO.setwarnings(False)
    
    GPIO.setup(LEFT_FWD, GPIO.OUT)
    GPIO.setup(LEFT_REV, GPIO.OUT)
    GPIO.setup(RIGHT_FWD, GPIO.OUT)
    GPIO.setup(RIGHT_REV, GPIO.OUT)
