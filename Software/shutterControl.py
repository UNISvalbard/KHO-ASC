# -*- coding: utf-8 -*-

"""
A small program to test the shutter and intensifier control

The shutter electronics has a simple watchdog mechanism, which requires
regular "petting". The computer will toggle a digital output, which will
open the shutter and power the image intensifier. If there is no change
in the signal for about one second, the relay will open and the shutter
will close and the intensifier power down.

In practical terms, writing any character to the serial port where the
ASC interface electronics is connected will open the shutter for about
a second. Note that the shutter/intensifier control box has a light
sensor, which prevents the shutter opening if there is too much ambient
light.


@author: MikkoS
"""

import serial
import time

# Serial port configuration
PORT = "/dev/ttyUSBX"
BAUDRATE = 115200
CHAR_TO_SEND = 'A'        # Does not really matter which character to send...
FREQUENCY_HZ = 1     
interval=1/FREQUENCY_HZ   # Send a character regularly when testing the electronics

# This is the routine to call regularly to keep the shutter open and intensifier powered
def pet_watchdog():
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            ser.write(CHAR_TO_SEND.encode('utf-8'))
    except serial.SerialException as e:
        print(f"Serial error: {e}")

# A test routine that will open the shutter and power the intensifier
# (run "python shutterControl.py" from command line)
def keep_open():
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            while True:
                ser.write(CHAR_TO_SEND.encode('utf-8'))
                time.sleep(interval)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Stopped by user.")

if __name__ == "__main__":
    print("ASC shutter control - keeping the shutter open")
    print("Press Control-C to interrupt")
    print()
    keep_open()
