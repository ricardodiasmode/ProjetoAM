import math

import pygame


def GetFirstGapDeltaLocation(car_loc, background):
    GapHeight = 0
    # Find gap height
    for i in range(int(car_loc[0]), 0, int(-background.BasicSquareSize)):
        if background.SquareDict[(0, i)] == "LOG" or \
                background.SquareDict[(64, i)] == "LOG":  # Searching two squares because one can be the gap
            GapHeight = i
            break
    for i in range(0, background.DisplayWidth, background.BasicSquareSize):
        if background.SquareDict[(i, GapHeight)] == "GRASS":
            Color = (255, 0, 0)
            pygame.draw.circle(background.Screen, Color,
                               (i, GapHeight),
                               7)
            return i - car_loc[0], GapHeight - car_loc[1]


def DistanceBetweenLocations(first_loc, second_loc):
    return math.sqrt((first_loc[0] - second_loc[0]) ** 2 + (
            first_loc[1] - second_loc[1]) ** 2)
