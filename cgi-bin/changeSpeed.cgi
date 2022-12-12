#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that changes the speed of the wheel motors,
#          regardless of current motor direction. This script requires one
#          input argument. The valid range is 0 to 1024, inclusive.
# 
#          changeSpeed.cgi requires ONE command line arguments:
#               - pwm speed control (0 to 1024)
# 
# EXAMPLE:
#       speedChange.cgi 512
#
#-----------------------------------------

expected_args=1
num_args=$# #number of arguments collected from the command line
reg_ex='^[0-9]+$' #regular expression that looks for non-negative integers
max_speed=1024

# First, check if the correct number of arguments have been supplied
# then assign 
if  (( $num_args >= $expected_args )) 
then
    
    speed=$1

    # check that supplied argument is a positive number
    if ! [[ $speed =~ $re ]]
    then
        echo "error: Not a number" >&2
        exit 1
    fi
    
    #second validity check
    if (( $1 > $max_speed))
    then
        $speed = $max_speed
    fi

    gpio pwm 1 $speed
    gpio pwm 26 $speed

else
    echo 'changeSpeed.cgi: ' $expectedargs 'argument required: pwm value'
    echo 'Example: changeSpeed.cgi {0-1024}'
fi

exit 0