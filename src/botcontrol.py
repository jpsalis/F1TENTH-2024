import serial
import time

"""
BotControl
Serial interface to Mega, sending, receiving and processing serial data.
"""


class BotControl:
    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 9600):
        self.ser = serial.Serial(port, baudrate, timeout=0.5)  # timeout
        self._armed = False  # Should be read only, set when update_telem called

        # Wait until serial is open.
        while not self.ser.is_open:
            time.sleep(0.01)

    def send(self, speed: int, steering: int) -> None:
        """Sends speed and steering values over serial to MEGA.
        Must be in the range -255 to 255."""
        if speed < -255 or speed > 255:
            raise RuntimeError("Speed value is invalid.")
        elif steering < -255 or steering > 255:
            raise RuntimeError("Steering value is invalid.")

        # TODO: Figure out how to make nonblocking
        message = f"{speed},{steering}\n"
        self.ser.write(message.encode(encoding="utf-8"))

    def update_telem(self) -> str:
        while self.ser.in_waiting:
            line = self.ser.readline().decode().lower()
            print(line)
            if "disarm" in line:
                self._armed = False
            elif "arm" in line:
                self._armed = True
            elif "failsafe" in line:
                print("Failsafe event")
            elif "error" in line:
                raise ValueError(f'Device report on input: "{line}"')

    @property
    def armed(self) -> bool:
        return self._armed


# Testing
def main():
    b = BotControl()
    while not b.armed:
        b.update_telem()
        time.sleep(0.01)

    for _ in range(10):
        b.send(0, 50)
        time.sleep(0.2)
        b.send(0, -50)
        time.sleep(0.2)

    b.send(0, 0)


if __name__ == "__main__":
    main()
