#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that turns the wheels opposite directions to
#          initiate a RIGHT turn.
#
#-----------------------------------------

source gpioVars.txt

gpio -g write $LEFT_FWD 1
gpio -g write $LEFT_REV 0
gpio -g write $RIGHT_FWD 0
gpio -g write $RIGHT_REV 1

# gpio -g write 5 1
# gpio -g write 6 0
# gpio -g write 13 0
# gpio -g write 19 1
