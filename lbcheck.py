#!/usr/bin/python
import RPi.GPIO as GPIO
import os
from lib import sim900
from datetime import datetime
from datetime import timedelta

cntFilePath = '.lbcheck'
lbPin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(lbPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lb = GPIO.input(lbPin)

if not os.path.exists(cntFilePath):
	f = open(cntFilePath, 'w')
  	f.write('0')
	f.close()

with open(cntFilePath, 'r') as cntFile:
	c = cntFile.readline().strip()

	if not c:
		cnt = 0
	else:
		cnt = int(c)

	if lb is 0:
	        with open('/proc/uptime', 'r') as u:
	                uptime_seconds = float(u.readline().split()[0])
	                uptime = str(timedelta(seconds = uptime_seconds))
	
		curtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		curtime = str(curtime)
	
		print '%s Battery low -> uptime is: %s' % (curtime, uptime)
		
		cnt += 1
		# Five consecutive low batteries. This prevent halting 
		# the sys due to a false positive
		if cnt >= 5:
			print 'Now halting system'
			# Turn off sim900
			if sim900.is_power_on():
				sim900.toggle_button(False)
			os.system("sudo shutdown -h now")	

if lb is 1 or cnt >= 5:
	cnt = 0

f = open(cntFilePath, 'w')	
f.write(str(cnt))
f.close()
