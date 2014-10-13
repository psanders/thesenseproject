#!/usr/bin/python
import time
from MPL115A2 import MPL115A2
import Adafruit_DHT
from datetime import timedelta

# Sensor DHT11 from Adafruit
sensor = Adafruit_DHT.DHT11
# Control pin the raspberry
pin = 25

STATION_ID = "S1"
GRID_LOCATION = "Unknown"

SAMPLE_DAYS = 1
SAMPLES_PER_HOUR = 6
SAMPLES = SAMPLES_PER_HOUR * 24 * SAMPLE_DAYS

def take_sample(sample):
        f = '/home/pi/wwrs/data/w%03d.txt' % sample

	with open('/proc/uptime', 'r') as u:
    		uptime_seconds = float(u.readline().split()[0])
		uptime_string = str(timedelta(seconds = uptime_seconds))

	with open(f, 'w') as file:
		file.write("StationId: %s\n" % STATION_ID)
		file.write("GridLocation: %s\n" % GRID_LOCATION)
		file.write("Datetime: %s\n" % time.strftime("%Y%m%d%H%M"))
		file.write("UpTime: %s\n" % uptime_string)
    		# Represents sensor MPL115A2
    		mp = MPL115A2()
    		# Take a temp and pressure sample
    		rList = mp.getPT()    
    		file.write("Temperature: %03.2fC\n" % rList[1])
    		file.write("Pressure: %03.2f hPa\n" % (rList[0] * 10.0))
    
    		# Take a temp and humidity
    		# Try to grab a sensor reading.  Use the read_retry method which will retry up
    		# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
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

# Take the samples
for sample in range(SAMPLES):
    # Note the time before the take
    start = time.time()
    take_sample(sample)
    # Wait for the next capture. Note that we take into
    # account the length of time it took to take the
    # sample when calculating the delay
    time.sleep(
        int(60 * 60 / SAMPLES_PER_HOUR) - (time.time() - start)
    )
