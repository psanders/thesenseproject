#!/usr/bin/python
import os, sys
from lib import common
import time as t

PROVIDER = "tmobile"

ifconfig = os.popen('ifconfig')
result = ifconfig.read()
ifconfig.close()

if "ppp" in result:
	sys.exit(0)

# Triple kill
try:
	os.system("poff %s" % PROVIDER)
	os.system('kill -9 $(pgrep -o pppd)') 
	os.system('rm -f /var/lock/LCK..ttyAMA0')
except: print "Good deal!"

t.sleep(5)

# Power cycle modem
common.toggle_button(False)
t.sleep(5)
common.toggle_button(True)
t.sleep(5)

# Using pppd notcha
os.system("pon tmobile")
