from math import floor
from rplidar import RPLidar

# Setup the RPLidar
PORT_NAME = "/dev/ttyUSB0"
lidar = RPLidar(PORT_NAME, timeout=3, baudrate = 115200)


# used to scale data to fit on the screen
max_distance = 0
MIN = 0
MAX = 20

def process_data(data):
    # Look for values in range, average sum of distance
    sum = 0
    count = 0
    for item in data:
        if item['angle'] >= MIN and item['angle'] <= MAX:
            sum += item['distance']
            count += 1
    if count > 0:
        print(sum / count)
            

scan_data = []
try:
    #    print(lidar.get_info())
    for scan in lidar.iter_scans():
        scan_data.clear()
        for _, angle, distance in scan:
            scan_data.append({'angle':min(359, floor(angle)), 'distance':distance})
        process_data(scan_data)

except KeyboardInterrupt:
    print("Stopping.")
lidar.stop()
lidar.disconnect()