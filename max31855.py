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
      for x in xrange(31,-1,-1):
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
      v = self.spiread32()
      if (v & 0x7):
         # uh oh, a serious problem!
         return float('nan')
      # get rid of internal temp data, and any fault bits
      v >>= 18
      # pull the bottom 13 bits off
      temp = v & 0x3FFF
      # check sign bit
      if (v & 0x2000):
         temp |= 0xC000
      celsius = v
      # LSB = 0.25 degrees C
      celsius *= 0.25
      celsius = celsius + self.offset
      return celsius
   
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
