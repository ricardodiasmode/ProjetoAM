import math


def GetClosestDistanceToLogs(character, log_locations):
    closest_distance = 9999999
    closest_index = 0
    for i in range(len(log_locations)):
        current_dist = DistanceBetweenLocations(character.CurrentLocation, log_locations[i])
        if closest_distance > current_dist:
            closest_distance = current_dist
            closest_index = i
    character.ClosestLogLocation = log_locations[closest_index]
    return abs(log_locations[closest_index][0] - character.CurrentLocation[0]), abs(log_locations[closest_index][1] - character.CurrentLocation[1])


def GetClosestDistanceToCharacters(character, other_characters):
    character_location = character.CurrentLocation
    closest_distance = 9999999
    closest_index = -1
    for i in range(len(other_characters)):
        if character.BlueTeamMember == other_characters[i].BlueTeamMember or other_characters[i].IsDead:
            continue
        current_dist = DistanceBetweenLocations(character_location, other_characters[i].CurrentLocation)
        if closest_distance > current_dist:
            closest_distance = current_dist
            closest_index = i
    if closest_index == -1:
        return 999, 999
    character.ClosestEnemy = other_characters[closest_index]
    return abs(other_characters[closest_index].CurrentLocation[0] - character_location[0]), \
        abs(other_characters[closest_index].CurrentLocation[1] - character_location[1])


def DistanceBetweenLocations(first_loc, second_loc):
    return math.sqrt((first_loc[0] - second_loc[0]) ** 2 + (
            first_loc[1] - second_loc[1]) ** 2)
