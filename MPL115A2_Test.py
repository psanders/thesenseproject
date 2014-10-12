#!/usr/bin/python

import time
from MPL115A2 import MPL115A2

mp = MPL115A2()

rList = mp.getPT()
print time.strftime("%Y-%b-%dT%H:%M:%S", time.localtime()), ":          Temerparture: %03.2f C" % rList[1]
print time.strftime("%Y-%b-%dT%H:%M:%S", time.localtime()), ":          Pressure: %03.2f hPa" % (rList[0] * 10.0)

