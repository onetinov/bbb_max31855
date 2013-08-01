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

NOTE: By default, users do not have access to /sys/class/gpio and any calls
to GPIO.setup() will cause the creation of new objects under /sys/class/gpio
that you also will not have access to.  As such the only way to run GPIO code
without root is to initialize the pins first and then recursively change 
permissions recursively (following links) throughout /sys/class/gpio.  You 
must then avoid any new calls to GPIO.setup.

The alternative is to just run everything as root, but understandably this
is a little disappointing.
