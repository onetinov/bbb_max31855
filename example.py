#! /usr/bin/python

import math,sys

sys.path.append('.')
from max31855 import MAX31855

# In this example, I have the following setup:
#
# data_pin = "GPIO1_15" # P8.15
# clk_pin = "GPIO1_14"  # P8.16
# cs_pin = "GPIO0_27"   # P8.17
#

therm = MAX31855("GPIO1_15","GPIO1_14","GPIO0_27")
tempintC = therm.readInternal()
tempintF = therm.CtoF(tempintC)
tempextC = therm.readCelsius()
tempextF = therm.readFarenheit()

if math.isnan(tempextC):
   print "Error reading Thermocouple - %s" % therm.readError()
else:
   print "Current internal temp = %.3f F, (%.3f C)" % (tempintF,tempintC)
   print "Current thermocouple temp = %.3f F, (%.3f C)" % (tempextF,tempextC)

