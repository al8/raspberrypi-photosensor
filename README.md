raspberrypi-photosensor
=======================

from:
  http://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading
use 100uF capacitor or larger for best results

prereqs:
  need GPIO
    http://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/necessary-packages
  sudo apt-get update
  sudo apt-get install python-dev
  sudo apt-get install python-rpi.gpio
  sudo apt-get install python-setuptools
  sudo easy_install rpi.gpio
  
setup:
  RUN these to get photosensor to run on startup:
  sudo cp initd_photosensor.sh /etc/init.d/
  sudo update-rc.d initd_photosensor.sh defaults
  sudo /etc/init.d/initd_photosensor.sh start
