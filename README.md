# roboberryPi

## The Plan

Create a small vehicle of some calibre controlled by a Raspberry Pi 3B.

The outside will have some kind of fun design (I haven't decided yet if I'm going 
to disassemble one of my kids' toys or just build from scratch and make it cute) 
but it will be all Raspberry under the hood. The Pi will host a server that 
supplies a webpage to the local network. This web page will be used to send 
commands to the Pi, controlling both the speed and direction.

I saw some suggestions that using scripts instead of Python to control the GPIO 
pins would result in faster, more real-time responses, so I will add code for 
both and test which version is faster.

## Components

- Raspberry Pi model 3B
- L298N motor driver
- 2 gear motors with wheels
- Solderless breadboard
- GPIO expansion board with GPIO cable(optional)
- Jumper wires (male-to-male and female-to-male)
- LEDs (for testing purposes - I used 2 yellow and 2 red)
- 330Ohm resistors (for testing purposes - as many as LEDs you have)

## Requirements

- Web server (RESTful API)
- Static web page
- Operational RPi vehicle
  - Drive forward and reverse
  - Turn left and right
  - At least 1 toggleable LED

## Wishlist
- Operatable camera attachment to see where you're driving
- Operates on WAN instead of LAN
- Handles multiple users


## The Execution

### Getting Started: The Physical Components

First, I created the .cgi Bash scripts (cgi-bin/) and the Python scripts 
(py-bin/). Then I wired up some LEDs on a breadboard to test that the scripts 
worked properly. By using red/yellow pairs of LEDs, I could see that the gpio 
pins were paired properly for running the motors.

![LED testing gif](assets/images/LED.gif)

Now that I knew the logic was correct, I tested wiring up each motor to make 
sure I had the motors correctly polarized (ie, they turn the wheels in the 
expected direction). I'm using a L298N motor driver to simplify the motor 
control. I also think it cuts down on the number of wires needed compared to 
using an L293D H bridge, as suggested in the [IoT Robot tutorial](#references).

![Wired up L298N motor driver](assets/images/L298N.jpg)


### Getting Started: The Browser Components

I decided to reuse a chunk of the web server I made for assignment 1. 


## References

1. The initial inspiration and the basis for all the .cgi scripts came from:
[IoT - Controlling a Raspberry Pi Robot Over Internet With HTML and Shell Scripts Only](https://www.instructables.com/IoT-Controlling-a-Raspberry-Pi-Robot-Over-Internet/) by Marcelo Rovai

2. The reference for the GPIO Python scripts:
[Control Raspberry Pi GPIO Pins from Python](https://www.ics.com/blog/control-raspberry-pi-gpio-pins-python) by Jeff Tranter