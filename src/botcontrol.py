"""
botcontrol Module
Contains BotControl class
"""
import time
import serial

class BotControl:
    """ 
    BotControl
    Serial interface to Mega, sending, receiving and processing serial data.

    parameters:
    armed: Current arm state received from the ESC/servo board

    methods:
    send(speed, steering):
    """
    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 9600):
        """Initialize serial and set internal variables."""
        self.ser = serial.Serial(port, baudrate, timeout=0.5)  # timeout
        self._armed = False  # Should be read only, set when update_telem called

        # Wait until serial is open.
        while not self.ser.is_open:
            time.sleep(0.01)

    def send(self, speed: int, steering: int) -> None:
        """Sends speed and steering values over serial.
       Values must be from -255 and 255 inclusive."""

        if speed < -255 or speed > 255:
            raise RuntimeError("Speed value is invalid.")
        if steering < -255 or steering > 255:
            raise RuntimeError("Steering value is invalid.")

        # TODO: Figure out how to make nonblocking
        message = f"{speed},{steering}\n"
        self.ser.write(message.encode(encoding="utf-8"))

    def update_telem(self) -> None:
        """Polls serial port for lines of incoming messages.
        Must be called frequently to ensure input doesn't 
        back up, and armstate is set correctly."""
        while self.ser.in_waiting:
            line = self.ser.readline().decode().lower()
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
        """Getter for internal armed variable."""
        return self._armed


def main():
    """Test for botcontrol Module"""
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
