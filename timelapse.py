#!/usr/bin/python
import sys
import fcntl
import time
import picamera
from lib import common
from fractions import Fraction
import logging
# This causes a conflict with cron
#import logging.config
#logging.config.fileConfig('logging.conf')
#logger = logging.getLogger('senseLogger')
logger = logging.getLogger(__name__)

VIDEO_DAYS = 1
FRAMES_PER_HOUR = 6
FRAMES = FRAMES_PER_HOUR * 24 * VIDEO_DAYS
DATA_FOLDER = '/home/pi/thesenseproject/data/'

if not common.lockFile('.lock.tl'):
	sys.exit(0)

logger.info("Starting tl")

def capture_frame(frame):
    with picamera.PiCamera() as cam:
        time.sleep(2)
	# Night options (De criteria must be refine, or add a light sensor)
	hour = int(time.strftime("%H")) 
	if hour > 18 or hour < 7:
		cam.framerate = Fraction(1, 6)
		cam.shutter_speed = 6000000
		cam.exposure_mode = 'off'
		cam.iso = 800

        cam.resolution = (1280, 720)
	t = int(time.strftime("%Y%m%d%H"))
        cam.capture(DATA_FOLDER + '%s_frame%03d.jpg' % (t, frame))

# Capture the images
for frame in range(FRAMES):
     
    # Note the time before the capture
    start = time.time()
    try:
    	capture_frame(frame)
    except Exception as e:
	logger.error(e)
	pass
    # Wait for the next capture. Note that we take into
    # account the length of time it took to capture the
    # image when calculating the delay
    time.sleep(
        int(60 * 60 / FRAMES_PER_HOUR) - (time.time() - start)
    )

