import serial
import time
import array

# AT cmds to initiate modem
CMD_AT = ["AT","OK"]  # First test if everything is okay.
CMD_AT_CPIN = ["AT+CPIN?", "+CPIN: READY"]  # This is to check if SIM is unlocked.
CMD_AT_CREG = ["AT+CREG?", "+CREG:"] # This checks if SIM is registered or not
CMD_AT_CGATT= ["AT+CGATT?", "+CGATT:"] # Check if GPRS is attached or not
INIT_SEC = [CMD_AT, CMD_AT_CPIN, CMD_AT_CREG, CMD_AT_CGATT]
# AT cmds to setup ftp client
CMD_AT_SAPBR_CONTENTTYPE = ["AT+SAPBR=3,1,\"Contype\",\"GPRS\"", "OK"]
CMD_AT_SAPBR_APN = ["AT+SAPBR=3,1,\"APN\",\"fast.t-mobile.com\"", "OK"]
CMD_AT_SAPBR_QUERY = ["AT+SAPBR=2,1", "OK"]
CMD_AT_FTPMODE = ["AT+FTPMODE=1", "OK"]
CMD_AT_FTPCID = ["AT+FTPCID=1", "OK"]
CMD_AT_FTPSERV = ["AT+FTPSERV=\"phonytive.com\"", "OK"]
CMD_AT_FTPPORT = ["AT+FTPPORT=21", "OK"]
CMD_AT_FTPPUN = ["AT+FTPUN=\"wwrsftp\"", "OK"]
CMD_AT_FTPPW = ["AT+FTPPW=\"G4t0p4rd0#\"", "OK"]
CMD_AT_FTPPUTNAME = ["AT+FTPPUTNAME=", "OK"] # You must add the file name !!!
CMD_AT_FTPPUTPATH = ["AT+FTPPUTPATH=\"/wwrsftp\"", "OK"]
CMD_AT_FTPPUT = ["AT+FTPGET=1", "OK"]
CMD_AT_FTPGETNAME = ["AT+FTPGETNAME=", "OK"] # You must add the file name !!!
CMD_AT_FTPGETPATH = ["AT+FTPGETPATH=\"/webroot/wwrftp\"", "OK"]

FTP_SEC = [CMD_AT_SAPBR_CONTENTTYPE, CMD_AT_SAPBR_APN, CMD_AT_SAPBR_QUERY, CMD_AT_FTPCID, CMD_AT_FTPSERV, CMD_AT_FTPPORT, CMD_AT_FTPPUN, CMD_AT_FTPPW, CMD_AT_FTPPUTPATH, CMD_AT_FTPGETPATH]

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
  return 0

# Initialize the modem
def init():
    for i in INIT_SEC:
        response = send_cmd(i, 2)
        print(response);
    
def setup_ftp():
    for i in FTP_SEC:
        response = send_cmd(i, 2);
        print(response);
def download_ftp(file):
    CMD_AT_FTPGETNAME[0] = CMD_AT_FTPGETNAME[0] + "\"" + file + "\""
    response = send_cmd(CMD_AT_FTPGETNAME, 2)
    print response
    response = send_cmd(CMD_AT_FTPPUT, 30)
    write("Blah blah")
def upload_ftp(file):
    CMD_AT_FTPPUTNAME[0] = CMD_AT_FTPPUTNAME[0] + "\"" + file + "\""
    response = send_cmd(CMD_AT_FTPPUTNAME, 2)
    print response
    response = send_cmd(CMD_AT_FTPPUT, 30)


# Initiate GPRS connection    
init()
# Setup ftp connection
setup_ftp()
    
while True:
    download_ftp("hello.txt")
    time.sleep(5000)
