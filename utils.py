import math


def GetClosestDistance(character_location, log_locations):
    closest_distance = 9999999
    closest_index = 0
    for i in range(len(log_locations)):
        current_dist = math.sqrt((character_location[0] - log_locations[i][0]) ** 2 + (
                character_location[1] - log_locations[i][1]) ** 2)
        if closest_distance > current_dist:
            closest_distance = current_dist
            closest_index = i

    return log_locations[closest_index]
