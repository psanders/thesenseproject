#!/usr/bin/python
import ftplib
import glob
import os, sys
import time
from shutil import move
from datetime import date
from lib import common
import logging
# This causes a conflict with cron
#import logging.config
#logging.config.fileConfig('logging.conf')
#logger = logging.getLogger('senseLogger')
logger = logging.getLogger(__name__)

SERVER = 'phonytive.com'
USER = 'wwrsftp'
PWD = 'G4t0p4rd0#'
DATA_DIR = "/home/pi/thesenseproject/data/"

if not common.lockFile(".lock.fs"):
	sys.exit(0)

while True:
	# Ensure dir exist
    	uploaded_files = DATA_DIR + str(date.today())
    	if not os.path.exists(uploaded_files):
        	os.mkdir(uploaded_files)

	try:
        	session = ftplib.FTP(SERVER, USER, PWD)
		session.cwd("wwrsftp")
		files = glob.glob(DATA_DIR + "*.txt")
		files += glob.glob(DATA_DIR + "*.jpg")

		# Max amount of files before reseting the fto session
		mf = 5	
		for f in files:
        		c = f.count("/")
        		fname = f.split("/")[c]
			file = open(f,'rb') 
			result = session.storbinary('STOR %s' % fname, file)
			file.close()
			if result:
				move(f, uploaded_files)
			mf -= 1
			if mv <= 0:
				break	
		session.quit()
	except:
		logger.error(e)
	time.sleep(60)

