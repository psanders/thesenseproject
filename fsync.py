mport serial
import time
import array

port = serial.Serial("/dev/ttyAMA0", baudrate = 115200, timeout = 2)

CMD_AT = ["AT","OK"]

def send_cmd(cmd):
  write(cmd)
  return read()

def read():
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch == '\r\n' or ch == '':
                return rv

def write(str):
        port.write(str + "\r\n")


response = send_cmd(CMD_AT)
print(response)
