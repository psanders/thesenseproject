import common as c
import time as t

for i in range(1,26):
	try:
		c.POWER_PIN = i
		print "trying with pin=" + str(i)
		c.toggle_button(True)
		t.sleep(1)
		if c.is_power_on() is True:
			print "Got it pin=" + str(i)
	except:	
		print "Exception?"
