"""Algorithm Module
Made for F1Tenth 2024"""


class Algorithm:
    """
    Given lidar information and previous data,
    chooses angle and speed the bot should use next.
    """

    def __init__(self):
        """initializes the class, and any features/variables required to operate."""

    # Could possibly take in more information depending on what sensors we add
    def process(self, lidar_data):
        """Returns motor and steering positions for bot to execute"""

        # TODO: Make test code that drives forward until an obstacle is in front

        sum = 0
        count = 0
        for _, angle, distance in lidar_data:
            if angle < 5 or angle > 355:
                count += 1
                sum += distance

        if count > 0:
            print(sum / count)

        return (0, 0)
