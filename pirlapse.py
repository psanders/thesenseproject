#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera
import datetime

sensorPin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prevState = False
currState = False

cam = picamera.PiCamera()
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
