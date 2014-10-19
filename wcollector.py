#!/usr/bin/python
import time
import Adafruit_DHT as dht
from lib import MPL115A2 as mpl
from datetime import timedelta

# Control PIN for the DHT11 sensor
DHT11_PIN = 25
STATION_ID = "s1"
GRID_LOCATION = "Unknown"

def take_sample():
	fn = time.strftime("%Y%m%d%H%M")        
        f = '/home/pi/thesenseproject/data/wc_%s.txt' % fn

	with open('/proc/uptime', 'r') as u:
    		uptime_seconds = float(u.readline().split()[0])
		uptime_string = str(timedelta(seconds = uptime_seconds))

	with open(f, 'w') as file:
		file.write("StationId: %s\n" % STATION_ID)
		file.write("GridLocation: %s\n" % GRID_LOCATION)
		file.write("Datetime: %s\n" % time.strftime("%Y%m%d%H%M"))
		file.write("UpTime: %s\n" % uptime_string)
    		# Sensor MPL115A2 object
    		mp = mpl.MPL115A2()
    		# Take a temp and pressure sample
    		rList = mp.getPT()    
    		file.write("Temperature: %03.2fC\n" % rList[1])
    		file.write("Pressure: %03.2f hPa\n" % (rList[0] * 10.0))
    
    		# Take a temp and humidity
    		# Try to grab a sensor reading.  Use the read_retry method which will retry up
    		# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    		humidity, temperature = dht.read_retry(dht.DHT11, DHT11_PIN)
    		# Note that sometimes you won't get a reading and
    		# the results will be null (because Linux can't
    		# guarantee the timing of calls to read the sensor).
    		# If this happens try again!
    		if humidity is not None and temperature is not None:
        		file.write('Temperature2: %0.1fC\n' % temperature)
			file.write('Humidity: %0.1f\n' % humidity)
    		else:
        		file.write('temp2: Unknown\n')
			file.write('humidity: Unknown\n')

take_sample()
 
