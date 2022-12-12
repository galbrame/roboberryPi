#!/bin/bash

#-----------------------------------------
# NAME: Megan Galbraith
# 
# REMARKS: A Bash script that turns an LED on or off. Requires one argument:
#          0 for "off," 1 for "on."
# 
# EXAMPLE:
#       led.cgi {0/1}
#
#-----------------------------------------

expected_args=1
num_args=$# #number of arguments collected from the command line
LED_gpio=10

if  (( $num_args >= $expected_args )) 
then
    gpio write $LED_gpio $1
else
    echo 'led.cgi: ' $expectedargs 'arguments required: off/on'
    echo 'Example: led.cgi {0/1}'
fi

exit 0
