import serial
import time
from .constants import ML_TO_SEC_RATIO
from .constants import ARDUINO_PORT
from .constants import ARM_PORT
import threading


def wait_for_arduino_response(arduino, expected="DONE"):
    while True:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            print(f"[Arduino] {response}")
            if expected in response:
                break

def stop_pin_after_delay(arduino,pin, delay_sec):
    time.sleep(delay_sec)
    stop_command = f"Ingredient {pin},0,0\n"
    arduino.write(stop_command.encode())
    print(f"🔽 Sent LOW for pin {pin}")



def wait_for_wheel_response(arduino, expected="Wheel done"):
    while True:
        try:
            response = arduino.readline().decode('utf-8', errors='ignore').strip()
            print(f"[Arduino] {response}")
            print(f"[Arduino repr] {repr(response)}")

            if "wheel done" in response.lower():
                print("✅ Found expected response.")
                break
        except Exception as e:
            print(f"[Serial Read Error] {e}")

# 


def wait_for_ingredient_responses(arduino, expected_prefix="Ingredient Finished", count=1):
    finished_pins = set()

    while len(finished_pins) < count:
        try:
            response = arduino.readline().decode('utf-8', errors='ignore').strip()
            print(f"[Arduino] {response}")
            print(f"[Arduino repr] {repr(response)}")

            if response.lower().startswith(expected_prefix.lower()):
                parts = response.split()
                if len(parts) == 3:
                    pin = parts[2]
                    if pin not in finished_pins:
                        finished_pins.add(pin)
                        print(f"✅ Ingredient finished for pin {pin}. ({len(finished_pins)}/{count})")

        except Exception as e:
            print(f"[Serial Read Error] {e}")


def wait_for_arm_response(arduino, expected="Garnish added!"):
    while True:
        if arduino.in_waiting > 0:
            try:
                raw = arduino.readline()
                decoded = raw.decode('utf-8', errors='ignore').strip()
                print(f"[Arduino] {decoded}")
                if expected in decoded:
                    print("✅ Found expected response.")
                    break
            except Exception as e:
                print(f"[Serial Read Error] {e}")



def callArduino(pins, garnishAngle):
    arduino = serial.Serial(ARDUINO_PORT, 9600, timeout=1)  # Update with your correct serial port
    # arduino2 = serial.Serial(ARM_PORT,9600,timeout = 1)
    # arduino2.setDTR(False)
    # arduino2.setRTS(False)
    time.sleep(2)  # Give some time for the Arduino to reset

    

    
    pin_list = list(pins.keys())
    pin_string = ",".join(str(pin) for pin in pin_list)
    command = f"StartPour {pin_string}\n"
    arduino.write(command.encode())
    print(f"🔼 Sent to Arduino: {command.strip()}")


    # wait_for_all_pour_responses(arduino,expected_prefix = 'Ingredient Poured',pins_expected=pins.keys())


    for pin, amount in pins.items():
        delay_sec = amount / ML_TO_SEC_RATIO
        threading.Thread(target=stop_pin_after_delay, args=(arduino,pin, delay_sec)).start()
            # Send the pin number and state as LOW (0), and include a placeholder for delay (e.g., 0)
    
    wait_for_ingredient_responses(arduino,expected_prefix = "Ingredient Finished",count = len(pins))

    command = f"Garnish {garnishAngle}\n"  # Sending garnish angle to Arduino for wheel rotation
    arduino.write(command.encode())  # Send command to Arduino
    print(f"Sent to Arduino: {command}")
    print("before")
    wait_for_wheel_response(arduino,expected = 'Wheel Done')
    print("after")

    # command = f'grab_garnish\n'
    # arduino2.write(command.encode())
    # print(f"Sent to arm: {command.strip()}")

    
    # wait_for_arm_response(arduino2,expected = "Garnish added!")

    command = f"Garnish Finish\n"  # Sending garnish angle to Arduino for wheel rotation
    arduino.write(command.encode())  # Send command to Arduino
    print(f"Sent to Arduino: {command}")



    arduino.close()
    # arduino2.close()
