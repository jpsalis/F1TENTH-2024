import serial

"""
BotControl
Serial interface to Mega, sending, receiving and processing serial data.
"""


class BotControl:
    def __init__(self, port="dev/ttyUSB0", baudrate=9600):
        self.ser = serial.Serial(
            port, baudrate, timeout=1
        )  # TODO: Determine good timeout

        # Print to serial that we're starting a connection
        self.ser.write(b"RESET")
        # TODO: Send a RESET signal to tell the mega to re-initialize

    # TODO: Could make asynchronous and send with a thread?
    def send(self, speed: int, steering: int):
        """Sends speed and steering values over serial to MEGA.
        Must be in the range -255 to 255."""
        if speed < -255 or speed > 255:
            raise RuntimeError("Speed value is invalid.")
        elif steering < -255 or steering > 255:
            raise RuntimeError("Steering value is invalid.")

        # TODO: Figure out how to make nonblocking
        self.ser.write(f"{speed},{steering}")

    def get_telem(self) -> str:
        # TODO: Read lines from serial in and send expected response back
        # Another class must be responsible for storing these values
        return ""

    def __del__(self):
        # Tells mega to set speed to zero and disconnect
        # Disconnects from serial
        self.ser.close()
