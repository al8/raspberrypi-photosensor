#!/usr/bin/env python
from __future__ import print_function
 
# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!
 
import argparse
import time
import sys
import atexit

import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)

g_RCpin = None

def RCtime (RCpin):
    global g_RCpin
    g_RCpin = RCpin

    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading

@atexit.register
def setread():
    if g_RCpin is None:
        return
    GPIO.setup(g_RCpin, GPIO.IN)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='photosensor, larger numbers are darker')
    parser.add_argument("--pin", type=int, default=18)
    parser.add_argument("--div", type=int, default=1)
    parser.add_argument("--outfile", "-o", type=str, default="/tmp/photosensor.value")
    parser.add_argument("--debug", action="store_true")
    options = parser.parse_args()

    if options.debug:
        print("using pin %d" % options.pin)

    while True:                                     
        reading = RCtime(options.pin) / options.div     # Read RC timing using pin #18
        if options.debug:
            print("%s: " % time.asctime(), file=sys.stderr, end='')
            print(reading)
        with open(options.outfile, "wb") as f:
            f.write("%d" % reading)
