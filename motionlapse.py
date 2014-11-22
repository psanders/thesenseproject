#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from lib import picam
from lib import common
import sys

sensorPin = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
currState = False

if not common.lockFile('.lock.pir'):
	sys.exit(0)

# Sensitivity control
hsecond = 0.5
cycles = 0
mThreshold = 2
oldState = False
currState= oldState

while True:
	time.sleep(hsecond)

	oldState = currState
	currState = GPIO.input(sensorPin)

	if currState is not oldState:
		# Adds half cycle
		cycles += 0.5
		print 'cycles=', cycles

		if cycles >= mThreshold:
			if not common.lockFile('.lock.cam'):
        			print 'Ohh we just miss an awesome pic :('
				continue

			print 'Photo time!'
			t = int(time.strftime("%Y%m%d%H%M%S"))
			result = picam.take_pic(common.DATA_FOLDER + 'm_%s.jpg' % t)
			cycles = 0	
		
			if result is False:
	        		print 'Ups something wrong with the camera'

			common.unlockFile('.lock.cam')
		continue	
	# Startover
	cycles = 0
	
