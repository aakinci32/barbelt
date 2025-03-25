import serial
import time
from .constants import ML_TO_SEC_RATIO
from .constants import ARDUINO_PORT
from .constants import ARM_PORT


def wait_for_arduino_response(arduino, expected="DONE"):
    while True:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            print(f"[Arduino] {response}")
            if expected in response:
                break

def wait_for_wheel_response(arduino,expected="Wheel Done"):
     while True:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            print(f"[Arduino] {response}")
            if expected in response:
                break

def wait_for_arm_response(arduino, expected="Garnish added!"):
    while True:
        if arduino.in_waiting > 0:
            try:
                raw = arduino.readline()
                decoded = raw.decode('utf-8', errors='ignore').strip()
                print(f"[Arduino] {decoded}")
                if expected in decoded:
                    break
            except Exception as e:
                print(f"[Serial Read Error] {e}")



def callArduino(pins, garnishAngle):
    arduino = serial.Serial(ARDUINO_PORT, 9600, timeout=1)  # Update with your correct serial port
    arduino2 = serial.Serial(ARM_PORT,9600,timeout = 1)
    arduino2.setDTR(False)
    arduino2.setRTS(False)
    time.sleep(2)  # Give some time for the Arduino to reset

    command = f"Garnish {garnishAngle}\n"  # Sending garnish angle to Arduino for wheel rotation
    arduino.write(command.encode())  # Send command to Arduino
    print(f"Sent to Arduino: {command}")

    # Read and print output from Arduino
    # while True:
    #     if arduino.in_waiting > 0:
    #         arduino_output = arduino.readline().decode().strip()
    #         if arduino_output:
    #             print(f"Arduino Output: {arduino_output}")
    #             break  # Exit loop after receiving output

    for pin, amount in pins.items():  # Iterate over the dictionary of pins and amounts
        delayAmount = amount / ML_TO_SEC_RATIO  # Calculate the delay based on amount in mL

        # Send the pin number, state (HIGH), and delay time (in seconds)
        command = f"Ingredient {pin},1,{delayAmount}\n"  # Include the delayAmount in the command
        arduino.write(command.encode())  # Send command to Arduino
        print(f"Sent to Arduino: {command}")  # Debug output
        time.sleep(2)  # Wait for the command to take effect

        # Read and print output from Arduino
        # while True:
        #     if arduino.in_waiting > 0:
        #         arduino_output = arduino.readline().decode().strip()
        #         if arduino_output:
        #             print(f"Arduino Output: {arduino_output}")
        #               # Exit loop after receiving output

        # Send the pin number and state as LOW (0), and include a placeholder for delay (e.g., 0)
        command = f"Ingredient {pin},0,0\n"   # Include a delay of 0 when turning the pin LOW
        arduino.write(command.encode())  # Send the command to Arduino
        print(f"Sent to Arduino: {command.strip()}")  # Debug output
        time.sleep(2)  # Wait for the command to take effect
    

    wait_for_wheel_response(arduino,expected = 'Wheel Done')
    command = f'grab_garnish\n'
    arduino2.write(command.encode())
    print(f"Sent to arm: {command.strip()}")


    wait_for_arm_response(arduino2,expected = "Garnish added!")

    command = f"Garnish Finish\n"  # Sending garnish angle to Arduino for wheel rotation
    arduino.write(command.encode())  # Send command to Arduino
    print(f"Sent to Arduino: {command}")



        # while True:
        #     if arduino.in_waiting > 0:
        #         arduino_output = arduino.readline().decode().strip()
        #         if arduino_output:
        #             print(f"Arduino Output: {arduino_output}")
        #             break  # Exit loop after receiving output

    arduino.close()
    arduino2.close()
