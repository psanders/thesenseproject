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

    files = glob.glob(DATA_DIR + "*.jpg")
    if len(files) == 0:
	print "Nothing to upload"
	time.sleep(S_T)
	continue

    print "Total files to upload:" + str(len(files))

    # Only do this the first time or SAPBR is close
    if is_ftp_setup is False or ftp.is_sapbr_open() is False:
	    retry = 5
	    while True:
	        result = ftp.setup()
	        if result is False:
		    print "Fail to setup ftp"
		    retry -= 1
	            time.sleep(5)
	            if retry is 0:
			# Power cicle modem after while
			common.toggle_button(False)
			time.sleep(10)
			common.toggle_button(True)
			time.sleep(10)
			retry = 5
		    continue
		is_ftp_setup = True
	        break 

    # Perform task here - upload files
    #files = glob.glob(DATA_DIR + "*.jpg")
    for f in files:
	c = f.count("/")
	fname = f.split("/")[c]
    	uploaded = ftp.upload(fname)
	if uploaded:
	    # Move to uploaded dir
	    move(f, uploaded_files)
	    continue
	break

    time.sleep(S_T)
