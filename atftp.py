import atio
import time
import os
from functools import partial

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

def upload_ftp(file):
    f = CMD_AT_FTPGETNAME
    f[0] = CMD_AT_FTPPUTNAME[0] + "\"" + file + "\""
    response = atio.send_cmd(f, 0.5)
    response = atio.send_cmd(CMD_AT_FTPPUT, 8) # It takes few seconds to open session
    if response == False:
	print "Can't upload file"
        # Close session if any
        response = atio.send_cmd(CMD_AT_FTPPUT_CLOSE, 0.5)
        print response
	return False
    # Read file to upload
    fsize = os.stat(DATA_FOLDER+file).st_size
    with open(DATA_FOLDER+file, 'r') as f:
        RECORD_SIZE = 1300
        records = iter(partial(f.read, RECORD_SIZE), b'')
        ccount = 0
    	for r in records:
    	    cmd = CMD_AT_FTPPUT_START[:]
    	    cmd[0] = cmd[0] + str(len(r))
	    print "Chunk #",ccount,"out of",fsize/1300, "and" ,(fsize - 1300 * ccount), "bytes left..."
	    ccount += 1
            # Upload file
    	    response = atio.send_cmd(cmd, 0.2)
    	    if response is not False:
	       atio.write(r)
	       err = atio.read()
	       if "ERROR" in err: return False
	response = atio.send_cmd(CMD_AT_FTPPUT_CLOSE, 0.5)
    return True

def setup_ftp():	
    for i in FTP_SEC:
        if i == CMD_AT_SAPBR_OPEN:
	   if is_sapbr_open() == True:
		continue
	   else:
                print "Starting SAPBR"
		response = atio.send_cmd(i, 0.5)
		if response is False:
			return False
		continue
        response = atio.send_cmd(i, 0.5);
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

