#!/usr/bin/python
import sys
import fcntl
import time
from lib import picam
from lib import common

DATA_FOLDER = '/home/pi/thesenseproject/data/'

if not common.lockFile('.lock.cam'):
	sys.exit(0)

t = int(time.strftime("%Y%m%d%H%M%S"))
result = picam.take_pic(DATA_FOLDER + '%s.jpg' % t)

if result is False:
	"Ups something wrong with the camera"
