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
    def process(self, lidar_data) -> tuple[int, int]:
        """Returns motor and steering positions for bot to execute"""

        # TODO: Make test code that drives forward at a constant speed
        # until an obstacle is in front with high probability
        return (0, 0)
