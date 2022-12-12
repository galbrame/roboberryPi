#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that sets two gpio pins to PWM mode.
#
#-----------------------------------------

# pin 18 is wPi 1
pwm_left=1
# pin 12 is wPi 26
pwm_right=26

gpio mode $pwm_left pwm
gpio mode $pwm_right pwm

exit 0