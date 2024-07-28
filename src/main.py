"""
Start point for processing computer.
Bot reads lidar data, processes it with an algorithm, and sends to microcontroller to handle servos.
"""
from algorithm import Algorithm
from botcontrol import BotControl
from lidar import Lidar
import time


""" SETUP """
# TODO: Both devices are TTYUSB, we need to figure out which is which somehow at runtime
lidar = Lidar("/dev/ttyLIDAR")
bot = BotControl("/dev/ttyUSB0")
hal_9000 = Algorithm()
state = "idle"


""" LOOP """
while True:
    # Reads incoming data from mega, stored as a string
    telem = bot.get_telem()

    # Sets state based on telemetry input
    if telem != "":
        state = telem

    if state == "running":
        reading = lidar.read()
        speed, angle = hal_9000.process(reading)
        bot.send(speed, angle)

    else:
        bot.send(0, 0)

    # Subject to change depending on implementation
    time.sleep(0.1)
