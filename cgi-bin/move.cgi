#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that controls the direction and speed of the
#          wheel motors. This file compiles the five previous control
#          scripts (forward.cgi, reverse.cgi, left.cgi, right.cgi, and
#          stop.cgi into a single script).
# 
#          move.cgi requires FIVE command line arguments:
#               - left wheel forward (0 or 1)
#               - left wheel reverse (0 or 1)
#               - right wheel forward (0 or 1)
#               - right wheel reverse (0 or 1)
#               - pwm speed control (0 to 1024)
# 
# BASIC EXAMPLES:
#       Forward motion: move.cgi 1 0 1 0 [>0]
#       Reverse motion: move.cgi 0 1 0 1 [>0]
#       Turn right:     move.cgi 1 0 0 1 [>0]
#       Turn left:      move.cgi 0 1 1 0 [>0]
# 
#       You can, of course, do other things, like turn while reversing,
#       but these are the most basic directional commands.
#
#-----------------------------------------

expected_args=5
num_args=$# #number of arguments collected from the command line

# First, check if the correct number of arguments have been supplied
# then assign 
if  (( $num_args >= $expected_args )) 
then

    left_fwd=$1
    left_rev=$2
    right_fwd=$3
    right_rev=$4
    speed=$5

    gpio -g write 5 $left_fwd
    gpio -g write 6 $left_rev
    gpio -g write 13 $right_fwd
    gpio -g write 19 $right_rev

    gpio pwm 1 $speed

else
    echo 'move.cgi: ' $expectedargs 'arguments required: left+, left-, right+, right-, pwm'
    echo 'Example: move.cgi {1/0}, {1/0}, {1/0}, {1/0}, {0-1024}'
fi

exit 0
