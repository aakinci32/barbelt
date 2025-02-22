import serial
import time

arduino = serial.Serial('/dev/tty.usbmodemXXXX',9600,timeout=1) #edit later once connected to arduino

time.sleep(2)
arduino.write(b'1')
time.sleep(10)
arduino.write(b'0')
time.sleep(1)
arduino.close()


