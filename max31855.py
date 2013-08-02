#! /usr/bin/python

import Adafruit_BBIO.GPIO as GPIO
from time import sleep

class MAX31855:
   def __init__(self, data_pin, clk_pin, cs_pin, offset=0):
      self.data = data_pin
      self.clk = clk_pin
      self.cs = cs_pin
      self.offset = offset

      GPIO.setup(self.cs, GPIO.OUT)
      GPIO.setup(self.clk, GPIO.OUT)
      GPIO.setup(self.data, GPIO.IN)

      GPIO.output(self.cs, GPIO.HIGH)
      GPIO.output(self.clk, GPIO.HIGH)
      
   def spiread32(self):
      d = 0
      GPIO.output(self.clk, GPIO.LOW)
      sleep(.01)
      GPIO.output(self.cs, GPIO.LOW)
      sleep(.01)
      for x in xrange(32,0,-1):
         GPIO.output(self.clk, GPIO.LOW)
         sleep(.01)
         d = d << 1
         if GPIO.input ( self.data ):
            d = d | 1
         GPIO.output(self.clk, GPIO.HIGH)
         sleep(.01)
      GPIO.output(self.cs, GPIO.HIGH)
      return d

   def readInternal(self):
      v = self.spiread32()
      # ignore bottom 4 bits - just thermocouple data
      v >>= 4
      internal = v & 0x7FF
      internal *= 0.0625 # LSB = 0.0625 degrees
      # check sign bit!
      if (v & 0x800):
        internal *= -1
      return internal

   def readCelsius(self):
      neg = False 
      cel = self.spiread32()
      cel = ((cel >> 18) & 0x3FFF) # Remove all but thermocouple data
      if ( cel & 0x2000 ):         # If we are reading negative...
         cel = -cel & 0x3FFF       # always work with positive valuesF
         neg = True                # record that it was negative
      cel = cel + 2                # Round up by .5 degC
      cel = cel >> 2               # convert from .25 units up to full degC
      if neg:
         cel = -cel                # invert if necessary
      return cel

   def CtoF(self,tinc):
      tinc *= 9.0
      tinc /= 5.0
      tinc += 32
      return tinc

   def readError(self):
      return self.spiread32() & 0x7
   
   def readFarenheit(self):
      f = self.readCelsius()
      f = self.CtoF(f)
      return f
