# F1TENTH-2024
Code for SUNY Plattsburgh F1TENTH 2024 competition

Arduino controls servo and ESC, receives serial commands from SOC using LIDAR data.

* Arduino controls PWM and receiver to prevent system crashes on Jetson from causing a runaway bot.
* Jetson reads LIDAR and uses SLAM algorithm to navigate around the course, avoiding obstacles.
* Bot shouldn't run if the transmitter had powered up with switch in the armed position.

Serial Syntax (Commands case-insensitive):

| Mode      | Command       | Connection  | Notes                                                                           |
|-----------|---------------|-------------|---------------------------------------------------------------------------------|
| Start     | ARM           | ARDU to JET | Jetson now controls bot                                                         |
| E-stop    | DISARM        | ARDU to JET | Jetson no longer has control, should pause accordingly                          |
| Bad Input | ERROR         | ARDU to JET | Should throw a runtime error when receieved                                     |
| Failsafe  | FAILSAFE      | ARDU to JET | Jetson didn't send inputs fast enough or crashed. Print for debugging or ignore|
| Command   | {thr},{steer} | JET to ARDU | Range: [-255, 255], subject to change                                           |

## Future Plans
Future plan for project is to run it with ROS2 Nodes, to better utilize the multiple threads and cores on the CPU.
