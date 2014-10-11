#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera
import datetime

def getFileName():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

sensorPin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prevState = False
currState = False

cam = picamera.PiCamera()
cnt = 0 
while True:
	time.sleep(.1)
	prevState = currState
	currState = GPIO.input(sensorPin)
	if currState != prevState:
		print "GPIO pin {0} is {1}".format(sensorPin, "HIGH" if currState else "LOW")
		if currState:
			fileName = str(cnt) + ".jpg"
			cnt += 1
			cam.capture(fileName)
			time.sleep(2)
