import serial
'''
BotControl
Serial interface to Mega, sending, receiving and processing serial data.
'''
class BotControl:
    def __init__(self, port = "dev/ttyUSB0", baudrate = 9600):
        self.port = port
        self.baudrate = baudrate
        # TODO: Print to serial that we're starting a connection
    
    # Both 
    def update(self, speed, steering):
        # Sends serial to mega to update speed and steering, -255 to 255, -255 to 255
        # Returns an error if speed or steering value is invalid
        pass
    
    def getStatus(self):
        # Makes a request to the mega for status info
        # Could have no change (None), "START", "STOP", "FAILSAFE", "INVALID_INPUT"
        # Another class is responsible for storing these values
        pass
    
        
    def __del__(self):
        # Tells mega to set speed to zero
        # Disconnects from serial
        pass
        
