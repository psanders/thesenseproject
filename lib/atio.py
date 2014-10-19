import serial
import time

# Sim900 modem
try:
    modem = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=0.1, writeTimeout=0.1)
except:
    modem = None

# Basic I/O operation: Read
def read():
    if modem is None:
        raise IOError("Modem busy")
    return modem.read(1024)

# Basic I/O operation: Read
def write(str):
    if modem is None:
        raise IOError("Modem busy")
    modem.write(str + "\r\n")

# Send a cmd an return a response or 0 in case off error
def send_cmd(cmd, timeout):
    write(cmd[0])
    time.sleep(timeout)
    response = read()
    if cmd[1] in response:
      return response
    return False
