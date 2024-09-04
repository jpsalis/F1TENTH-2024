"""Algorithm Module
Made for F1Tenth 2024"""


class Algorithm:
    """
    Given lidar information and previous data,
    chooses angle and speed the bot should use next.
    """

    def __init__(self):
        """initializes the class, and any features/variables required to operate."""
        self.running = True
        self.sample_volume = 10

    # Could possibly take in more information depending on what sensors we add
    def process(self, lidar_data):
        """Returns motor and steering positions for bot to execute"""

        # TODO: Make test code that drives forward until an obstacle is in front

        sum = 0
        count = 0
        farthest_point = (0, 0) # angle, distance
        points = []
        for _, angle, distance in lidar_data:
            points.append((angle, distance))

            if angle < 5 or angle > 355:
                count += 1
                sum += distance
                

        """print("current distance", distance, angle)
            if angle < 90 or angle > 270:
                if farthest_point[0] < distance:
                    farthest_point = (distance, angle)
                
        print("farthest point",farthest_point)
        """
        max_avg_dist = 0
        # Code to determine angle to follow
        if len(points) > self.sample_volume:
            for i in range(len(points)):
                dist_sum = 0
                for j in range(self.sample_volume):
                    dist_sum += points[(i + j) % len(points)][1]

                avg_dist = dist_sum / self.sample_volume

                # TODO: Also ensure the angle is within valid cone
                if avg_dist > farthest_point[1]: 
                    #TODO: Change to average of points, counting overflow at 0 and 360
                    farthest_point = (
                            points[(i + self.sample_volume // 2) % len(points)][0],
                            avg_dist
                            )

        print("angle:", farthest_point[0], "distance:", farthest_point[1])
        # Convert farthest point and angle to distance
                    
                    


        # count > 0 needed to prevent divide-by-zero error
        if count > 0:
            distance = sum/count
            #print("distance", distance)
            if distance < 400:
                self.running = False
            
        if self.running:
            return (25, 0)

        #print("shut off")
        return (-200, 0)
