import serial
import time

def callArduino(pins):
    arduino = serial.Serial('/dev/tty.usbmodemXXXX', 9600, timeout=1)  # Update with your correct serial port
    time.sleep(2)  # Give some time for the Arduino to reset

    for pin in pins:  # Iterate over the list of pins to send
        # For each pin, send the pin number and state (1 for HIGH, 0 for LOW)
        command = f"{pin},1\n"  # Send the pin number and state as HIGH (1)
        arduino.write(command.encode())  # Send command to Arduino
        print(f"Sent to Arduino: {command.strip()}")  # Debug output
        time.sleep(2)  # Wait for the command to take effect

        # Optionally turn the pin LOW after some time (or you could control it as per your requirement)
        command = f"{pin},0\n"  # Send the pin number and state as LOW (0)
        arduino.write(command.encode())  # Send the command to Arduino
        print(f"Sent to Arduino: {command.strip()}")  # Debug output
        time.sleep(2)  # Wait for the command to take effect
    
    arduino.close()


