#!/usr/bin/env python
 
# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!
 
import argparse
import time

import RPi.GPIO as GPIO
 
DEBUG = 1
GPIO.setmode(GPIO.BCM)
 
def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='photosensor, larger numbers are darker')
    parser.add_argument("--pin", type=int, default=18)
    parser.add_argument("--outfile", "-o", type=str, default="/tmp/photosensor.value")
    parser.add_argument("--debug", action="store_true")
    options = parser.parse_args()

    if options.debug:
        print("using pin %d" % options.pin)

    while True:                                     
        reading = RCtime(options.pin)     # Read RC timing using pin #18
        if options.debug:
            print(reading)
        with open(options.outfile, "wb") as f:
            f.write("%d" % reading)
