#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that sets the wheels in REVERSE motion
#
#-----------------------------------------

source gpioVars.txt

gpio -g write $LEFT_FWD 0
gpio -g write $LEFT_REV 1
gpio -g write $RIGHT_FWD 0
gpio -g write $RIGHT_REV 1

# gpio -g write 5 0
# gpio -g write 6 1
# gpio -g write 13 0
# gpio -g write 19 1
