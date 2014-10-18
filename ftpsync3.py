import ftplib
import glob
import os
from shutil import move
from datetime import date

server = "phonytive.com"
user = "wwrsftp"
password = "G4t0p4rd0#"

DATA_DIR = "/home/pi/wwrs/data/"

while True:
	# Ensure dir exist
    	uploaded_files = DATA_DIR + str(date.today())
    	if os.path.exists(uploaded_files) is False:
        	os.mkdir(uploaded_files)

        session = ftplib.FTP(server, user, password)

	files = glob.glob(DATA_DIR + "*.txt")
	files += glob.glob(DATA_DIR + "*.jpg")
	
	for f in files:
		print "sending %s" % f
        	c = f.count("/")
        	fname = f.split("/")[c]
		file = open(f,'rb') 
		try:
			result = session.storbinary('STOR %s' % fname, file)
			file.close()
			if result:
				move(f, uploaded_files)
		except:
			"Failed to upload"    
	session.quit()
