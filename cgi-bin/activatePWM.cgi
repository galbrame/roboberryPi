#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that sets two gpio pins to PWM mode.
#
#-----------------------------------------

# pin 18 is wPi 1
pwm_left=1
# pin 23 is wPi 4
pwm_right=4

gpio mode pwm_left pwm
gpio mode pwm_right pwm

exit 0