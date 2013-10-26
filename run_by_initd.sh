#!/bin/bash
echo 0 > /tmp/photosensor.value
chown -R pi /tmp/photosensor.value
chgrp -R pi /tmp/photosensor.value
((/home/pi/raspberrypi-photosensor/photosensor.py -o /tmp/photosensor.value 2>&1) & echo $! >&3) 3> $1 &
