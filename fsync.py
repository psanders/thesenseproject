import serial
import time
import array
import RPi.GPIO as GPIO

# Commands to perform FTP transfer
CMD_AT = ["AT","OK"]  # First test if serial connection up
CMD_AT_SAPBR_CLOSE = ["AT+SAPBR=0,1", "OK"]
CMD_AT_SAPBR_OPEN = ["AT+SAPBR=1,1", "OK"]
CMD_AT_SAPBR_CONTENTTYPE = ["AT+SAPBR=3,1,\"Contype\",\"GPRS\"", "OK"]
CMD_AT_SAPBR_APN = ["AT+SAPBR=3,1,\"APN\",\"wap.cingular\"", "OK"]
CMD_AT_SAPBR_USER = ["AT+SAPBR=3,1,\"USER\",\"WAP@CINGULARGPRS.COM\"", "OK"]
CMD_AT_SAPBR_PWD = ["AT+SAPBR=3,1,\"PWD\",\"CINGULAR1\"", "OK"]
CMD_AT_SAPBR_QUERY = ["AT+SAPBR=2,1", "+SAPBR: 1,1,"]
CMD_AT_FTPCID = ["AT+FTPCID=1", "OK"]
CMD_AT_FTPSERV = ["AT+FTPSERV=\"phonytive.com\"", "OK"]
CMD_AT_FTPPORT = ["AT+FTPPORT=21", "OK"]
CMD_AT_FTPPUN = ["AT+FTPUN=\"wwrsftp\"", "OK"]
CMD_AT_FTPPW = ["AT+FTPPW=\"G4t0p4rd0#\"", "OK"]
CMD_AT_FTPPUTNAME = ["AT+FTPPUTNAME=", "OK"] # You must add the file name !!!
CMD_AT_FTPPUTPATH = ["AT+FTPPUTPATH=\"wwrsftp/\"", "OK"]
CMD_AT_FTPPUT = ["AT+FTPPUT=1", "OK"]
CMD_AT_FTPGETNAME = ["AT+FTPGETNAME=", "OK"] # You must add the file name !!!
CMD_AT_FTPGETPATH = ["AT+FTPGETPATH=\"wwrsftp/\"", "OK"]
CMD_AT_FTPGET = ["AT+FTPGET=1", "+FTPGET:1,1"]
FTP_SEC = [CMD_AT_SAPBR_CLOSE, CMD_AT_SAPBR_CONTENTTYPE, CMD_AT_SAPBR_APN, CMD_AT_SAPBR_USER, CMD_AT_SAPBR_PWD, CMD_AT_SAPBR_OPEN, CMD_AT_SAPBR_QUERY, CMD_AT_FTPCID, CMD_AT_FTPSERV, CMD_AT_FTPPORT, CMD_AT_FTPPUN, CMD_AT_FTPPW, CMD_AT_FTPPUTPATH, CMD_AT_FTPGETPATH]

# Sim900 modem
port = serial.Serial("/dev/ttyAMA0", baudrate = 115200, writeTimeout = 2)

# Basic I/O operation: Read
def read():
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if len(ch) == 0:
                return rv
# Basic I/O operation: Read
def write(str):
    port.write(str + "\r\n")

# Send a cmd an return a response or 0 in case off error
def send_cmd(cmd, timeout):
  port.timeout = timeout
  write(cmd[0])
  response = read()

  if cmd[1] in response:
    return response
  # Debugging response
  print response
  return False

def setup_ftp():
    for i in FTP_SEC:
        response = send_cmd(i, 2);
        print(response);
        # Something is wrong
        if response == False:
            return False

def download_ftp(file):
    f = CMD_AT_FTPGETNAME
    f[0] = CMD_AT_FTPGETNAME[0] + "\"" + file + "\""
    response = send_cmd(f, 2)
    print response
    response = send_cmd(CMD_AT_FTPGET, 5)
    print response
    if response != False:
        write("AT+FTPGET=2,1024") # FTPGET MODE 2
        data_size = int(port.readline().rsplit(",")[1])
        print "--"
        print port.read(data_size)
        print "--"
    # Must verify if download is OK and them place the data in a file
    return False

def upload_ftp(file):
    f = CMD_AT_FTPGETNAME
    f[0] = CMD_AT_FTPPUTNAME[0] + "\"" + file + "\""
    response = send_cmd(f, 2)
    print response
    response = send_cmd(CMD_AT_FTPPUT, 30)

def reset_modem():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, True)
    time.sleep(2)
    GPIO.output(12, False)
    
# Do this forever    
while True:
    while(True):
        is_ftp_setup = setup_ftp();
        if is_ftp_setup == False:
            print "Something when wrong w/ setting up the ftp setup. Let's start over!"
            continue
        break
    download_completed = download_ftp("readme.txt")
    if download_completed == False:
        print "Something went wrong..."
    
    # Lets do this all over again
    time.sleep(60)
