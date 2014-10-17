#!/usr/bin/python
import os
import fcntl
import time
import RPi.GPIO as GPIO
import logging
import atio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POWER_PIN = 15
CMD_AT = ["AT","OK"]

def lockFile(lockfile):
    fd = os.open(lockfile, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return False

    return True

def toggle_button(on):
    logger.info('Turning %s modem' % on)
    if on != is_power_on():
    	GPIO.setwarnings(False)
    	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(POWER_PIN, GPIO.OUT) 
    	GPIO.output(POWER_PIN, True) 
    	time.sleep(2)
    	GPIO.output(POWER_PIN, False) 

def is_power_on():
        try:
                response = atio.send_cmd(CMD_AT, 0.5)
                if response is not False:
                        return True
        except:
		logger.error('Modem busy')
                return True

	return False

