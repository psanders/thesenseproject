#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera
import datetime
from fractions import Fraction

sensorPin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prevState = False
currState = False

cam = picamera.PiCamera()
#cam.led = False
cam.resolution = (1280, 720)
# Set a framerate of 1/6fps, then set shutter
# speed to 6s and ISO to 800
cam.framerate = Fraction(1, 6)
cam.shutter_speed = 6000000
cam.exposure_mode = 'off'
cam.iso = 800

frame = 0 
while True:
	time.sleep(.1)
	prevState = currState
	currState = GPIO.input(sensorPin)
	if currState != prevState:
		print "GPIO pin {0} is {1}".format(sensorPin, "HIGH" if currState else "LOW")
		if currState:
			fileName = ('/home/pi/wwrs/data/frame%03d.jpg' % frame)
			frame += 1
			cam.capture(fileName)
			time.sleep(2)
