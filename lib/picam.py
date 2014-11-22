#!/usr/bin/python
import fcntl
import picamera
import time
from fractions import Fraction


def take_pic(n):
    with picamera.PiCamera() as cam:
        cam.resolution = (640, 480)
        # Night options (A criteria must be refine, or add a light sensor)
        hour = int(time.strftime("%H"))
	# Test this with the NoIR
        if hour > 18 or hour < 7:
        	cam.framerate = Fraction(1, 6)
        	cam.shutter_speed = 3000000
        	cam.exposure_mode = 'off'
        	cam.iso = 800

	#cam.image_effect = 'cartoon'
		
	# Black & White
	cam.color_effects = (128, 128)
	try:
        	cam.capture(n)
	except:
		return False
