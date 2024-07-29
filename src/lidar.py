"""Lidar Module
Made for F1Tenth 2024"""
# Unimplemented and unnecesary until ROS2 setup
from adafruit_rplidar import RPLidar


class Lidar:
    """Wrapper class for adafruit rplidar, useful for a consistent interface
    Handles lidar parsing, converting to a usable type, and safe input handling on crash"""

    def __init__(self, port="dev/ttyUSB0", baudrate=115200, timeout=3):
        self.lidar = RPLidar(None, port, baudrate, timeout)
        pass


        # Value will be Iterator[Tuple[bool, int|None, float, float]]

    def __del__(self):
        # TODO: Create a way to safely disconnect and
        # shutoff the lidar if the program is abruptly shutdown with ctrl C or otherwise.
        pass
