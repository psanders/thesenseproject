#!/usr/bin/python
import atio
import time
import os
import logging
from functools import partial
from sys import stdout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Commands to perform FTP transfer
CMD_AT = ["AT","OK"]  # First test if serial connection up
CMD_AT_SAPBR_CLOSE = ["AT+SAPBR=0,1", "OK"]
CMD_AT_SAPBR_OPEN = ["AT+SAPBR=1,1", "OK"]
CMD_AT_SAPBR_CONTENTTYPE = ["AT+SAPBR=3,1,\"Contype\",\"GPRS\"", "OK"]
CMD_AT_SAPBR_APN = ["AT+SAPBR=3,1,\"APN\",\"fast.t-mobile.com\"", "OK"]
CMD_AT_SAPBR_USER = ["AT+SAPBR=3,1,\"USER\",\"\"", "OK"]
CMD_AT_SAPBR_PWD = ["AT+SAPBR=3,1,\"PWD\",\"\"", "OK"]
CMD_AT_SAPBR_QUERY = ["AT+SAPBR=2,1", "0.0.0.0"]
CMD_AT_FTPCID = ["AT+FTPCID?", ""]
CMD_AT_FTPSERV = ["AT+FTPSERV=\"phonytive.com\"", "OK"]
CMD_AT_FTPPORT = ["AT+FTPPORT=21", "OK"]
CMD_AT_FTPTYPE = ["AT+FTPTYPE=\"I\"", "OK"]
CMD_AT_FTPPUN = ["AT+FTPUN=\"wwrsftp\"", "OK"]
CMD_AT_FTPPW = ["AT+FTPPW=\"G4t0p4rd0#\"", "OK"]
CMD_AT_FTPPUTNAME = ["AT+FTPPUTNAME=", "OK"] # You must add the file name !!!
CMD_AT_FTPPUTPATH = ["AT+FTPPUTPATH=\"wwrsftp/\"", "OK"]
CMD_AT_FTPPUT = ["AT+FTPPUT=1", "+FTPPUT:1,1"]
CMD_AT_FTPPUT_START = ["AT+FTPPUT=2,", "+FTPPUT:2,"]
CMD_AT_FTPPUT_CLOSE = ["AT+FTPPUT=2,0", "+FTPPUT:2,0"]
CMD_AT_FTPGETNAME = ["AT+FTPGETNAME=", "OK"] # You must add the file name !!!
CMD_AT_FTPGETPATH = ["AT+FTPGETPATH=\"wwrsftp/\"", "OK"]
CMD_AT_FTPGET = ["AT+FTPGET=1", "+FTPGET:1,1"]
FTP_SEC = [CMD_AT, CMD_AT_SAPBR_CONTENTTYPE, CMD_AT_SAPBR_APN, CMD_AT_SAPBR_USER, CMD_AT_SAPBR_PWD, CMD_AT_SAPBR_OPEN, CMD_AT_FTPCID, CMD_AT_FTPSERV, CMD_AT_FTPPORT, CMD_AT_FTPTYPE, CMD_AT_FTPPUN, CMD_AT_FTPPW, CMD_AT_FTPPUTPATH, CMD_AT_FTPGETPATH]
DATA_FOLDER = "/home/pi/wwrs/data/"

MAX_CHUNK_RETRY = 50.00

def upload(file):
    f = CMD_AT_FTPGETNAME
    f[0] = CMD_AT_FTPPUTNAME[0] + "\"" + file + "\""
    response = atio.send_cmd(f, 0.5)
    response = atio.send_cmd(CMD_AT_FTPPUT, 20) # It takes few seconds to open session
    if response == False:
	logger.warning("Fail to open ftp session")
	atio.send_cmd(CMD_AT_FTPPUT_CLOSE, 15)
	return False
    # Read file to upload
    fsize = os.stat(DATA_FOLDER + file).st_size
    start = time.time()
    with open(DATA_FOLDER+file, 'r') as f:
	
        RECORD_SIZE = 1300
        records = list(iter(partial(f.read, RECORD_SIZE), b''))	
	i = 0
	p = 0
    	while i < len(records):
    	    cmd = CMD_AT_FTPPUT_START[:]
    	    cmd[0] = cmd[0] + str(len(records[i]))
            plost = float(p/MAX_CHUNK_RETRY) * 10

	    upercent = int ((float(i) / len(records)) * 100)
    	    stdout.write("\rUpload percent: %d%%" % upercent) 
	    stdout.flush()

            # Upload file
	    if plost < 5:
		tout = 0.05
	    if plost > 10:
		tout = 0.08
	    if plost > 25:
		tout > 1
	    if plost > 35:
		tout = 1.5
	    if plost > 40:
		tout = 2
	    if plost > 60:
		tout = 2.5
	    if plost > 75:
		tout = 3
	    if plost > 90:
		tout = 8

    	    response = atio.send_cmd(cmd, tout)
	    atio.writeTimeout = tout
    	    if response is not False:
	       atio.write(records[i])
	       err = atio.read()
	       if "ERROR" in err:
			return False
	       i += 1
	       if p > 1:
	      		p -= 1
	       continue
            p += 1
	    # Let it recover
	    time.sleep(2)
	    if p > MAX_CHUNK_RETRY:
	 	return False
	time.sleep(5)
	response = atio.send_cmd(CMD_AT_FTPPUT_CLOSE, 10)
    ft = time.time()-start
    logger.info("\nUpload time:" + str(ft))
    return True

def setup():
    # Ensure there is not a prior ftp session
    atio.send_cmd(CMD_AT_FTPPUT_CLOSE, 10)
    for cmd in FTP_SEC:
	if cmd == CMD_AT_FTPSERV:
		response = atio.send_cmd(cmd, 10)
        	if response == False:
            		return False
		continue
        if cmd == CMD_AT_SAPBR_OPEN:
	   if is_sapbr_open() == True:
		continue
	   else:
                logging.info("Starting SAPBR")
		response = atio.send_cmd(cmd, 20)
		if response is False:
			return False
		continue
        response = atio.send_cmd(cmd, 0.5);
        # Something is wrong
        if response == False:
            return False
    return True

# Move this to common
def is_sapbr_open():
    response = atio.send_cmd(CMD_AT_SAPBR_QUERY, 0.5)
    if response == False:
	return True
    return False

