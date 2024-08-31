"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar
import time

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((1000,1000))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, baudrate=115200, timeout=3)

# used to scale data to fit on the screen
max_distance = 0

#pylint: disable=redefined-outer-name,global-statement
def process_data(data):

    global max_distance
    lcd.fill((255,255,255))
    for _, angle, distance in data:
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * sin(radians)
            y = distance * -cos(radians)
            point = (500 + int(x / max_distance * 500), 500 + int(y / max_distance * 500))
            lcd.set_at(point, pygame.Color(0, 0, 0))
    pygame.display.update()

def main():
    try:
        for scan in lidar.iter_scans():
            process_data(scan)

    except KeyboardInterrupt:
        print('Stopping.')

    lidar.stop()
    lidar.disconnect()

main()

