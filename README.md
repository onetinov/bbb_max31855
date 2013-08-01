bbb_max31855
============

Introduction

Whilst moving from my Arduino to my Beaglebone Black I found no working
python libraries for interacting with the MAX31855 thermocouple amplifier.
https://github.com/alexanderhiam/PyBBIO looked promising, but is broken
for 3.8 linux kernels.

As such, I have written an extremely simplistic framework to get basic
data out of the MAX31855.  All of the concepts in the code come directly
from here: https://github.com/adafruit/Adafruit-MAX31855-library

Full credit goes to the Adafruit team who created the BeagleBone IO Python 
Library that this project depends on.

https://github.com/adafruit/adafruit-beaglebone-io-python

NOTE: By default, users do not have access to /sys/class/gpio, as such
you may want to start by either changing permissions on that directory
tree, or running the python code as root.  I did the following:

Created a "gpio" user group and added my user to it.
Refreshed my group membership by starting a new shell.
Ran the following - 
  "sudo chown -Rh root:gpio /sys/class/gpio"
  "sudo chmod -R g+w /sys/class/gpio"

I take no responsibility if this sets your beaglebone on fire and your
house falls into the ocean.  There is almost certainly a more granular
way to approach permissions such as running an strace on the example
code and looking for gpio permission denied errors.
