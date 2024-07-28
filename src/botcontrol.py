import serial
import time

"""
BotControl
Serial interface to Mega, sending, receiving and processing serial data.
"""


class BotControl:
    def __init__(self, port="/dev/ttyACM0", baudrate=9600):
        self.ser = serial.Serial(
            port, baudrate, timeout=0.5
        )  # TODO: Determine good timeout
        time.sleep(3)
        # Sleep until connection made

        #self.ser.write(b"RESET")

        # Print to serial that we're starting a connection
        # TODO: Send a RESET signal to tell the mega to re-initialize

    def send(self, speed: int, steering: int):
        """Sends speed and steering values over serial to MEGA.
        Must be in the range -255 to 255."""
        if speed < -255 or speed > 255:
            raise RuntimeError("Speed value is invalid.")
        elif steering < -255 or steering > 255:
            raise RuntimeError("Steering value is invalid.")

        # TODO: Figure out how to make nonblocking
        message = f"{speed},{steering}\n"
        self.ser.write(message.encode())

    def get_telem(self) -> str:
        # TODO: Read lines from serial in and send expected response back
        # Another class must be responsible for storing these values
        #return self.ser.read_until('\n')
        return self.ser.in_waiting


    def __del__(self):
        # Tells mega to set speed to zero and disconnect
        # Disconnects from serial
        pass

def main():
    b = BotControl()
    for i in range(500):
        b.send(0, 255)
        time.sleep(0.5)

    b.send(0, 0)


if __name__ == "__main__":
    main()