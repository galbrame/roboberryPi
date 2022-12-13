#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that sets two gpio pins to PWM mode.
#
# NOTE: Setting the PWM pin modes at boot time doesn't seem to translate
#       through to proper functionality for the user, so use this once
#       past boot mode to get it to work as expected (see README.md for
#       more details).
#
#-----------------------------------------

# pin 18 is wPi 1
pwm_left=1
# pin 12 is wPi 26
pwm_right=26

gpio mode $pwm_left pwm
gpio mode $pwm_right pwm

exit 0