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

