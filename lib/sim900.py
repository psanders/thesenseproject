import os
import fcntl
import time
import RPi.GPIO as GPIO
import logging
import atio

POWER_PIN = 15
CMD_AT = ["AT","OK"]
CMD_AT_CSQ = ["AT+CSQ", "+CSQ:"]

def lockFile(lockfile):
    	fd = os.open(lockfile, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
    	try:
        	fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    	except IOError:
        	return False

    	return True

def get_signal():
	try:
		response = atio.send_cmd(CMD_AT_CSQ, 0.5)
	except:
		return False
def toggle_button(on):
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
                return True

	return False

