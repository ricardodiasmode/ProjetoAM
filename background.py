from random import randrange

import pygame.display


class Background:
    DisplayWidth = 1280
    DisplayHeight = 720
    BasicSquareSize = 64
    Screen = None
    LogLocations = []
    SquareImageDict = {}
    SquareDict = {}

    Grass0Img = pygame.image.load('Grass0.png')
    Grass1Img = pygame.image.load('Grass1.png')
    Grass2Img = pygame.image.load('Grass2.png')
    Grass3Img = pygame.image.load('Grass3.png')

    def __init__(self):
        self.screen = pygame.display.set_mode((self.DisplayWidth, self.DisplayHeight + 50))
        self.LogLocations = []
        self.SquareImageDict = {}
        self.SquareDict = {}
        self.drawBackground()

    def drawBackground(self):
        LogImg = pygame.image.load('Log.png')

        # filling background with grass
        for currentHeight in range(0, self.DisplayHeight, self.BasicSquareSize):
            for currentWidth in range(0, self.DisplayWidth, self.BasicSquareSize):
                randomNumber = randrange(4)
                ImageToUse = self.Grass0Img
                if randomNumber == 1:
                    ImageToUse = self.Grass1Img
                elif randomNumber == 2:
                    ImageToUse = self.Grass2Img
                elif randomNumber == 3:
                    ImageToUse = self.Grass3Img
                self.screen.blit(ImageToUse, (currentWidth, currentHeight))
                self.SquareImageDict[(currentWidth, currentHeight)] = ImageToUse
                self.SquareDict[(currentWidth, currentHeight)] = "GRASS"

        # drawing logs
        for currentHeight in range(0, self.DisplayHeight, self.BasicSquareSize):
            for currentWidth in range(0, self.DisplayWidth, self.BasicSquareSize):
                randomNumber = randrange(10)
                if 4 >= randomNumber > 2:
                    self.screen.blit(LogImg, (currentWidth, currentHeight))
                    self.SquareImageDict[(currentWidth, currentHeight)] = LogImg
                    self.SquareDict[(currentWidth, currentHeight)] = "LOG"
                    self.LogLocations.append((currentWidth, currentHeight))
