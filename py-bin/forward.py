#!/bin/python3

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Python script that sets the wheels in FORWARD motion
#
#-----------------------------------------

import RPi.GPIO as GPIO
import projectSetup as PROJ

PROJ.gpioSetup()

# GPIO.setmode(GPIO.BCM)

# # shouldn't have to do this because set at start up
# GPIO.setup(PROJ.LEFT_FWD, GPIO.OUT)
# GPIO.setup(PROJ.LEFT_REV, GPIO.OUT)
# GPIO.setup(PROJ.RIGHT_FWD, GPIO.OUT)
# GPIO.setup(PROJ.RIGHT_REV, GPIO.OUT)

GPIO.output(PROJ.LEFT_FWD, 1)
GPIO.output(PROJ.LEFT_REV, 0)
GPIO.output(PROJ.RIGHT_FWD, 1)
GPIO.output(PROJ.RIGHT_REV, 0)
