#!/usr/bin/python

#===========================================================================
# Code based off yaso.kuhl post in forum and adafruit_support_mike
# modified and restructured by kkkkkbruce
#===========================================================================

import time
import RPi.GPIO as GPIO
from Adafruit_I2C import Adafruit_I2C

#===========================================================================
# Adafruit MPL115A2 Class
#===========================================================================

class MPL115A2 :
    __i2c = None

    # Registers
    __MPL115A2_Padc_MSB = 0x00
    __MPL115A2_Padc_LSB = 0x01
    __MPL115A2_Tadc_MSB = 0x02
    __MPL115A2_Tadc_LSB = 0x03
    __MPL115A2_a0_MSB   = 0x04
    __MPL115A2_a0_LSB   = 0x05
    __MPL115A2_b1_MSB   = 0x06
    __MPL115A2_b1_LSB   = 0x07
    __MPL115A2_b2_MSB   = 0x08
    __MPL115A2_b2_LSB   = 0x09
    __MPL115A2_c12_MSB  = 0x0A
    __MPL115A2_c12_LSB  = 0x0B
    __MPL115A2_CONVERT  = 0x12

    __outpin = 0

    def __init__(self, address=0x60, outpin=4, debug=False):
        MPL115A2.__i2c = Adafruit_I2C(address)
        MPL115A2.__outpin = outpin
        MPL115A2.debug = debug
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__outpin, GPIO.OUT)
        self.wakeup()
        # Start conversion
        MPL115A2.__i2c.write8(self.__MPL115A2_CONVERT, 0)
        # Wait for conversion to complete
        time.sleep(0.003)
        # Read registers for coefficients - only needs to be done once
        self.a0_temp = (MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_a0_MSB) << 8)  + MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_a0_LSB)
        self.b1_temp = (MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_b1_MSB) << 8) + MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_b1_LSB)
        self.b2_temp = (MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_b2_MSB) << 8) + MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_b2_LSB)
        self.c12_temp = (MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_c12_MSB) << 8) + MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_c12_LSB)
        self.sleep()

        def parse_coefficient(coeff, div, offset=0): # see data sheet pg 5 & 6
            #Thanks to Mike at Adafruit and the forums for help with this!
            coeff &= 0xfffe                    #strip last bit
            if coeff & 0x8000:                 #signed bit present
                coeff ^= 0xffff                #invert bits
                coeff *= -1                    #negate
            coeff = coeff >> offset            #shift un-used bits
            return float(coeff)/div            #covert to frac & move dec. point
        
        self.a0 = parse_coefficient(self.a0_temp, 0x8)
        self.b1 = parse_coefficient(self.b1_temp, 0x2000)
        self.b2 = parse_coefficient(self.b2_temp, 0x4000)
        self.c12 = parse_coefficient(self.c12_temp, 0x400000,2)
        
        if debug:
            print "coefficient  a0 = ", self.a0
            print "coefficient  b1 = ", self.b1
            print "coefficient  b2 = ", self.b2
            print "coefficient c12 = ", self.c12

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def cleanup(self):
        GPIO.cleanup()
        
    def getPT(self):
        self.wakeup()  # Start conversion
        MPL115A2.__i2c.write8(self.__MPL115A2_CONVERT, 0)  # Wait for conversion to complete
        time.sleep(0.003)
        # Read registers
        self.Padc_tmp = (MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_Padc_MSB) << 8) + MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_Padc_LSB)
        self.Tadc_tmp = (MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_Tadc_MSB) << 8) + MPL115A2.__i2c.readU8(MPL115A2.__MPL115A2_Tadc_LSB)
        self.sleep()

        # Getting Padc
        self.Padc = (self.Padc_tmp & 0xFFC0) >> 6
        if self.debug:
            print "Padc: %04i (0x%04X)" % (self.Padc, self.Padc)

        # Getting Tadc
        self.Tadc = (self.Tadc_tmp & 0xFFC0) >> 6
        if self.debug:
            print "Tadc: %04i (0x%04X)" % (self.Tadc, self.Tadc)

        self.Pcomp = self.a0 + (self.b1 + self.c12 * self.Tadc) * self.Padc + self.b2 * self.Tadc
        if self.debug:
            print "Pcomp: ", self.Pcomp

        self.Tcomp = ((self.Tadc - 498.0) / -5.35 + 25.0)
        self.Pcomp = ((self.Pcomp * ((115.0 - 50.0) / 1023.0)) + 50.0 )
        self.Lreturn = [self.Pcomp, self.Tcomp]
        return self.Lreturn

    def sleep(self):
        GPIO.output(MPL115A2.__outpin, False)
        time.sleep(0.005)

    def wakeup(self):
        GPIO.output(MPL115A2.__outpin, True)
        time.sleep(0.005)
