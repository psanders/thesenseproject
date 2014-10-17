import serial
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Sim900 modem
try:
    print "DBg`"
    modem = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=0.1, writeTimeout=0.1)
    print "modem %s=" % modem
    
except:
    print "DBG2"
    logger.error("Modem busy")
    modem = None

# Basic I/O operation: Read
def read():
    if modem is None:
        logger.error("Modem busy") 
        raise IOError("Modem busy")
    return modem.read(1024)

# Basic I/O operation: Read
def write(str):
    if modem is None:
	logger.error("Modem busy") 
        raise IOError("Modem busy")
    modem.write(str + "\r\n")

# Send a cmd an return a response or 0 in case off error
def send_cmd(cmd, timeout):
    write(cmd[0])
    time.sleep(timeout)
    response = read()
    logger.debug("[")
    logger.debug(response)
    logger.debug("]")
    if cmd[1] in response:
      return response
    return False
