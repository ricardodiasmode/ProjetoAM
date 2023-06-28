import math


def GetFirstGapDeltaLocation(car_loc, background):
    GapHeight = 0
    # Find gap height
    for i in range(int(car_loc[0]), 0, int(-background.BasicSquareSize)):
        if background.SquareDict[(i, 0)] == "LOG" or \
                background.SquareDict[(i + 64, 0)] == "LOG":  # Searching two squares because one can be the gap
            GapHeight = i
            break
    for i in range(0, background.DisplayWidth, background.BasicSquareSize):
        if background.SquareDict[(i, GapHeight)] == "GRASS":
            return i, GapHeight


def DistanceBetweenLocations(first_loc, second_loc):
    return math.sqrt((first_loc[0] - second_loc[0]) ** 2 + (
            first_loc[1] - second_loc[1]) ** 2)
