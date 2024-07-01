# F1TENTH-2024
Code for SUNY Plattsburgh F1TENTH 2024 competition

Arduino controls servo and ESC, receives serial commands from Raspberry pi with camera vision and/or lidar.

* Arduino controls PWM and receiver to prevent system crashes on Pi from causing a runaway bot.
* Rpi reads LIDAR and uses SLAM algorithm to navigate around the course, avoiding obstacles.
