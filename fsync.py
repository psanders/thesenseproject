import serial
import time
import array

RETRY = 3
# AT CMDS
CMD_AT = ["AT","OK"]  # First test if everything is okay.
CMD_AT_CPIN = ["AT+CPIN?", "+CPIN: READY"]  # This is to check if SIM is unlocked.
CMD_AT_CREG = ["AT+CREG?", "+CREG:"] # This checks if SIM is registered or not
CMD_AT_CGATT= ["AT+CGATT?", "+CGATT:"] # Check if GPRS is attached or not
CMD_AT_CIPSHUT = ["AT+CIPSHUT", "SHUT OK"] # Reset the IP session if any
CMD_AT_CIPSTATUS = ["AT+CIPSTATUS", "STATE: IP INITIAL"] # Check if the IP stack is initialized
CMD_AT_CIPMUX = ["AT+CIPMUX=0", "OK"] # Single connection mode
CMD_AT_CSTT = ["AT+CSTT=\"fast.t-mobile\",\" \",\" \"", "OK"] # Start the task, based on the SIM card you are using
CMD_AT_CIICR = ["AT+CIICR", "OK"] # Bring wireless up
CMD_AT_CIFSR = ["AT+CIFSR", "."] # Get the local IP address.
INIT_SEC = [CMD_AT, CMD_AT_CPIN, CMD_AT_CREG, CMD_AT_CGATT, CMD_AT_CIPSHUT, CMD_AT_CIPSTATUS, CMD_AT_CIPMUX, CMD_AT_CSTT, CMD_AT_CIICR, CMD_AT_CIFSR]

# Sim900 modem
port = serial.Serial("/dev/ttyAMA0", baudrate = 115200, timeout = 10)

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
def send_cmd(cmd):
  write(cmd[0])
  response = read()

  if cmd[1] in response:
    return response
  return 0

def is_connection_alive():
  response = send_cmd(CMD_AT_CIPSTATUS) 
  print(response)
  if send_cmd(CMD_AT_CIPSTATUS) is not 0:
    return True
  return False

# Initialize the modem
def init():
  for i in INIT_SEC:
    response = send_cmd(i);
    print(response);
    
while True:
  init()
  if is_connection_alive():
    # Try to connect to a random server
    cmd = ["AT+CIPSTART=\"TCP\",\"astivetoolkit.org\",\"80\"", ""]
    response = send_cmd(cmd);
    print(response)
    print(is_connection_alive())
  else:
    init()
  # Check again in 60 secs
  time.sleep(30000)
