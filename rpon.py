#!/usr/bin/python
import os, sys
import collections
from lib import common
from lib import sim900
import time as t
import logging

# This causes a conflict with cron
#import logging.config
#logging.config.fileConfig('logging.conf')
#logger = logging.getLogger('senseLogger')
logger = logging.getLogger(__name__)

if not common.lockFile(".lock.rp"):
	sys.exit(0)

PROVIDER = 'tmobile'
DEVICE = '/dev/ttyAMA0'

# Power cycle modem
sim900.toggle_button(False)
sim900.toggle_button(True)

t.sleep(5)

if not sim900.is_power_on():
	logger.error("Modem is off")
	sys.exit(0)

i = 10
while True:
	ifconfig = os.popen('ifconfig')
	result = ifconfig.read()
	ifconfig.close()

	if "ppp" in result:
		sys.exit(0)

	logger.warn("pppd is not up")

	# Triple kill
	try:
		os.system('poff %s' % PROVIDER)
		t.sleep(15)
		os.system('kill -9 $(pgrep -o pppd)') 
		os.system('rm -f /var/lock/LCK..ttyAMA0')
		# XXX: AttributeError and TypeError may occur
		result = os.popen('fuser %s' % DEVICE)
		if result:
			list = result.split()
			for l in list:
				if l is not "/dev/ttyAMA0:":
					os.system("kill -9 %s" % l)

	except Exception as e:
		logger.error(e)
		pass

	t.sleep(5)
	os.system("pon %s" % PROVIDER)
	t.sleep(5)

	i -= 1
	if i == 0:
		logger.info("Turning process off")
		sys.exit(0)
