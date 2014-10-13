#!/usr/bin/python
# Execute on @reboot

import os
import time
import glob
import atftp as ftp
import atio
import common
from shutil import move
from datetime import date
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 60 secs?
S_T = 60
DATA_DIR = "/home/pi/wwrs/data/"

# Ensure modem is on
common.toggle_button(True)

is_ftp_setup = False

while True:	
    # Ensure dir exist
    uploaded_files = DATA_DIR + str(date.today())
    if os.path.exists(uploaded_files) is False:
	os.mkdir(uploaded_files)

    files = glob.glob(DATA_DIR + "*.txt")
    files += glob.glob(DATA_DIR + "*.jpg")
    
    if len(files) == 0:
	logger.info("Nothing to upload")
	time.sleep(S_T)
	continue

    logger.info("Files to upload " + str(len(files)))

    # Only do this the first time or SAPBR is close
    if is_ftp_setup is False or ftp.is_sapbr_open() is False:
	    logger.info("Setting up ftp")
	    retry = 5
	    while True:
	        result = ftp.setup()
	        if result is False:
		    logger.warning("Fail to setup ftp")
		    retry -= 1
	            time.sleep(5)
	            if retry is 0:
			# Power cicle modem after while
			logger.info("Power cycling gprs module") 
			common.toggle_button(False)
			time.sleep(10)
			common.toggle_button(True)
			time.sleep(10)
			retry = 5
		    continue
		is_ftp_setup = True
	        break 

    # Perform task here - upload files
    h = 0
    hr = 0
    logger.info("Uploading file")
    while h < len(files):
	f = files[h] 
	c = f.count("/")
	fname = f.split("/")[c]
    	uploaded = ftp.upload(fname)
	if uploaded:
	    # Move to uploaded dir
	    move(f, uploaded_files)
	    h += 1
	    continue
	hr += 1
	if hr >= 5:
		break

    time.sleep(S_T)
