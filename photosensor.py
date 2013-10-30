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

def RCtime (RCpin, sleep, maxvalue):
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
        time.sleep(sleep)
        if reading >= maxvalue: break
    return reading

@atexit.register
def setread():
    if g_RCpin is None:
        return
    GPIO.setup(g_RCpin, GPIO.IN)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='photosensor, resistor/capacitor timer method. larger numbers are darker, default values tuned for 3uF capacitor.')
    parser.add_argument("--pin", type=int, default=18, help="gpio pin used")
    parser.add_argument("--div", type=int, default=1, help="divide final value by this")
    parser.add_argument("--sleep", type=float, default=0.04, help="sleep between counter in counting")
    parser.add_argument("--maxvalue", type=int, default=50, help="max 'darkness' to be detected")
    parser.add_argument("--outfile", "-o", type=str, default="/tmp/photosensor.value")
    parser.add_argument("--debug", action="store_true")
    options = parser.parse_args()

    if options.debug:
        print("using pin %d" % options.pin)

    while True:                                     
        reading = RCtime(options.pin, options.sleep, options.maxvalue) / options.div     # Read RC timing using pin #18
        if options.debug:
            print("%s: " % time.asctime(), file=sys.stderr, end='')
            print(reading)
        with open(options.outfile, "wb") as f:
            f.write("%d" % reading)
        time.sleep(0.5)
