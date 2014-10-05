#!/usr/bin/python
# Execute on @reboot
import os
import time
import glob
import atftp
import atio
import common
from shutil import move
from datetime import date

# 60 secs
S_T = 10
DATA_DIR = "/home/pi/wwrs/data/"

# Ensure modem is on
common.toggle_button(True)

while True:
    # Ensure dir exist
    uploaded_files = DATA_DIR + str(date.today())
    if os.path.exists(uploaded_files) is False:
        os.mkdir(uploaded_files)

    retry = 5
    while True:
        result = atftp.setup_ftp()
        if result == False:
            print "Can't setup ftp"
            retry -= 1
            time.sleep(5)
            print "Lets try again"
            if retry is 0:
                # Power cicle modem
                common.toggle_button(False)
                time.sleep(3)
                common.toggle_button(True)
            continue
        break

    # Perform task here - upload files
    files = glob.glob(DATA_DIR + "*.jpg")
    for f in files:
        c = f.count("/")
        fname = f.split("/")[c]
        uploaded = atftp.upload_ftp(fname)
        if uploaded:
            # Move to uploaded dir
            move(f, uploaded_files)
            continue
        break

    time.sleep(S_T)
