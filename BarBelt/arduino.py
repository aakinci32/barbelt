import serial
import time
from .constants import ML_TO_SEC_RATIO

def callArduino(pins):
    
    
    
    
    
    arduino = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=1)  # Update with your correct serial port
    time.sleep(2)  # Give some time for the Arduino to reset

    for pin, amount in pins.items():  # Iterate over the dictionary of pins and amounts
        delayAmount = amount / ML_TO_SEC_RATIO  # Calculate the delay based on amount in mL

        # Send the pin number, state (HIGH), and delay time (in seconds)
        command = f"{pin},1,{delayAmount}\n"  # Include the delayAmount in the command
        arduino.write(command.encode())  # Send command to Arduino
        print(f"Sent to Arduino: {command.strip()}")  # Debug output
        time.sleep(2)  # Wait for the command to take effect

        # Send the pin number and state as LOW (0), and include a placeholder for delay (e.g., 0)
        command = f"{pin},0,0\n"  # Include a delay of 0 when turning the pin LOW
        arduino.write(command.encode())  # Send the command to Arduino
        print(f"Sent to Arduino: {command.strip()}")  # Debug output
        time.sleep(2)  # Wait for the command to take effect

    arduino.close()
