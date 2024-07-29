"""
Start point for processing computer.
Bot reads lidar data, processes it with an algorithm, and sends to microcontroller to handle servos.
"""

from algorithm import Algorithm
from botcontrol import BotControl
from adafruit_rplidar import RPLidar
import time

LIDAR_PORT = "/dev/ttyUSB0"  # Subject to change, should be set with a udev rule
MEGA_PORT = "/dev/ttyACM0"  # Subject to change, should be set with a udev rule


""" SETUP """
lidar = RPLidar(None, LIDAR_PORT, baudrate=115200, timeout=3)
bot = BotControl(MEGA_PORT, baudrate=115200)
hal_9000 = Algorithm()

if lidar.health() == "Error" or lidar.health == "Warning":
    lidar.reset()

lidar.start_motor()


""" LOOP """
prev_armed = False

try:
    while True:
        if bot.armed:
            # Things to do while bot is armed
            # TODO: Might need to clear input depending on speed of algorithm?
            speed, angle = hal_9000.process(lidar.iter_scans())
            bot.send(speed, angle)
        else:
            # Things to do while the bot is disarmed
            pass

        if not bot.armed and prev_armed:
            # Things to do when bot has just disarmed
            lidar.stop()
            pass

        prev_armed = bot.armed
        bot.update_telem()
        time.sleep(0.1)

except KeyboardInterrupt:
    lidar.stop()
    lidar.disconnect()
