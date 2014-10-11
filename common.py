#!/usr/bin/python
import RPi.GPIO as GPIO 
import time
import atio
import atftp

POWER_PIN = 15
CMD_AT = ["AT","OK"]

def toggle_button(on):
    if on != is_power_on():
    	GPIO.setwarnings(False)
    	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(POWER_PIN, GPIO.OUT) 
    	GPIO.output(POWER_PIN, True) 
    	time.sleep(2)
    	GPIO.output(POWER_PIN, False) 

def is_power_on():
    response = atio.send_cmd(CMD_AT, 0.5)
    if response is not False:
	return True
    return False

