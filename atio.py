import serial
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sim900 modem
modem = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=0.1, writeTimeout=0.1)

# Basic I/O operation: Read
def read():
    return modem.read(1024)

# Basic I/O operation: Read
def write(str):
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

