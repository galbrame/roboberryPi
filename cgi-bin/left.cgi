#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that turns the wheels opposite directions to
#          initiate a LEFT turn.
#
#          Although using `source` to pull in variables works just fine
#          executing the script from the command line, it doesn't seem to
#          work when launching the script through Python ("gpioVars.txt: No
#          such file or directory"), so this is my compromise until I
#          refactor my code.
#
#-----------------------------------------

# source gpioVars.txt

# gpio -g write $LEFT_FWD 0
# gpio -g write $LEFT_REV 1
# gpio -g write $RIGHT_FWD 1
# gpio -g write $RIGHT_REV 0

gpio -g write 5 0
gpio -g write 6 1
gpio -g write 13 1
gpio -g write 19 0
