from random import randrange

import pygame.display


class Background:
    RoundsWithoutSpawningLog = 2
    MinRoundsToSpawnLog = 3
    MaxRoundsToSpawnLog = 5
    DisplayWidth = 1024
    DisplayHeight = 1024
    BasicSquareSize = 64
    Screen = None
    SquareImageDict = {}
    SquareDict = {}
    LastGapLocation = -1

    Grass0Img = pygame.image.load('Grass0.png')
    Grass1Img = pygame.image.load('Grass1.png')
    Grass2Img = pygame.image.load('Grass2.png')
    Grass3Img = pygame.image.load('Grass3.png')
    LogImg = pygame.image.load('Log.png')

    def __init__(self):
        self.Screen = pygame.display.set_mode((self.DisplayWidth + 275, self.DisplayHeight))
        self.LogLocations = []
        self.SquareImageDict = {}
        self.SquareDict = {}
        self.InitBackground()

    def InitBackground(self):
        # filling background with grass
        for currentWidth in range(0, self.DisplayWidth, self.BasicSquareSize):
            for currentHeight in range(0, self.DisplayHeight, self.BasicSquareSize):
                randomNumber = randrange(4)
                ImageToUse = self.Grass0Img
                if randomNumber == 1:
                    ImageToUse = self.Grass1Img
                elif randomNumber == 2:
                    ImageToUse = self.Grass2Img
                elif randomNumber == 3:
                    ImageToUse = self.Grass3Img
                self.Screen.blit(ImageToUse, (currentWidth, currentHeight))
                self.SquareImageDict[(currentWidth, currentHeight)] = ImageToUse
                self.SquareDict[(currentWidth, currentHeight)] = "GRASS"

    def DrawBackground(self):
        randomNumber = randrange(1, 3)
        if (self.RoundsWithoutSpawningLog > self.MinRoundsToSpawnLog and
                randomNumber == 1) or self.RoundsWithoutSpawningLog > self.MaxRoundsToSpawnLog:
            self.RedrawBackground(True)
            self.SpawnLog()
            HalfDisplayWidth = (self.DisplayWidth / 2)/64
            self.RoundsWithoutSpawningLog = -HalfDisplayWidth + 2
            return
        else:
            self.RedrawBackground(False)
            self.RoundsWithoutSpawningLog += 1
            return

    def SpawnLog(self):
        if self.LastGapLocation == -1:
            GapLocation = self.DisplayWidth/2
        else:
            MinGapLocation = self.LastGapLocation - (self.RoundsWithoutSpawningLog * 64)
            MaxGapLocation = self.LastGapLocation + (self.RoundsWithoutSpawningLog * 64)

            if MinGapLocation < 0:
                MinGapLocation = 0
            if MaxGapLocation > self.DisplayWidth - 64:
                MaxGapLocation = self.DisplayWidth - 64

            GapLocation = randrange(MinGapLocation, MaxGapLocation, self.BasicSquareSize)
        self.LastGapLocation = GapLocation
        for currentWidth in range(0, self.DisplayWidth, self.BasicSquareSize):
            if currentWidth == GapLocation:
                continue
            self.SquareDict[(currentWidth, 0)] = "LOG"
            self.SquareImageDict[(currentWidth, 0)] = self.LogImg
            self.Screen.blit(self.SquareImageDict[(currentWidth, 0)], (currentWidth, 0))

    def RedrawBackground(self, log_spawned):
        for i, j in reversed(list(self.SquareDict)):
            if j == self.DisplayHeight:
                continue
            self.SquareDict[(i, j + 64)] = self.SquareDict[(i, j)]
            self.SquareImageDict[(i, j + 64)] = self.SquareImageDict[(i, j)]
            self.Screen.blit(self.SquareImageDict[(i, j + 64)], (i, j + 64))
        if not log_spawned:
            for i in range(0, self.DisplayWidth, self.BasicSquareSize):
                randomNumber = randrange(4)
                ImageToUse = self.Grass0Img
                if randomNumber == 1:
                    ImageToUse = self.Grass1Img
                elif randomNumber == 2:
                    ImageToUse = self.Grass2Img
                elif randomNumber == 3:
                    ImageToUse = self.Grass3Img
                self.Screen.blit(ImageToUse, (i, 0))
                self.SquareImageDict[(i, 0)] = ImageToUse
                self.SquareDict[(i, 0)] = "GRASS"
