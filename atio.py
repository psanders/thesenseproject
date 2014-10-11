import serial
import time

# Sim900 modem
port = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, timeout=0.5, writeTimeout=2)

# Basic I/O operation: Read
def read():
    return port.read(1024)

# Basic I/O operation: Read
def write(str):
    port.write(str + "\r\n")

# Send a cmd an return a response or 0 in case off error
def send_cmd(cmd, timeout):
  write(cmd[0])
  time.sleep(timeout)
  response = read()
  print "{", response, "}"
  if cmd[1] in response:
    return response
  return False

