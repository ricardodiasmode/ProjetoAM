
import math


def get_closest_location(location_to_compare, locations_array):
    closest_location_index = 0
    closest_distance = 9999999
    for i in range(len(locations_array)):
        current_dist = math.sqrt((location_to_compare[0] - locations_array[i][0]) ** 2 + (
                location_to_compare[1] - locations_array[i][1]) ** 2)
        if closest_distance > current_dist:
            closest_distance = current_dist
            closest_location_index = i
    return closest_location_index


def any_location_equal(location_to_compare, locations_array):
    for i in range(len(locations_array)):
        if location_to_compare == locations_array[i]:
            return True
    return False
