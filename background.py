import pygame
from random import randrange
from enum import Enum


class Background:
    SquareType = Enum('SquareType', ['GRASS', 'LOG', 'TREE', 'ROCK', 'TENT', 'CHICKEN', 'RIVER'])

    display_width = 1280
    display_height = 720
    basic_square_size = 64
    screen = None

    def __init__(self):
        self.screen = pygame.display.set_mode((self.display_width, self.display_height + 50))

    def drawBackground(self):
        # loading images
        grass0Img = pygame.image.load('Grass0.png')
        grass1Img = pygame.image.load('Grass1.png')
        grass2Img = pygame.image.load('Grass2.png')
        grass3Img = pygame.image.load('Grass3.png')
        chickenImg = pygame.image.load('Galinha.png')
        treeImg = pygame.image.load('Tree.png')
        logImg = pygame.image.load('Log.png')
        rockImg = pygame.image.load('Rock.png')

        # filling background with grass
        SquareDict = {
            (0, 0): 'GRASS'
        }

        currentHeight = 0
        currentWidth = 0
        while currentHeight < self.display_height:
            while currentWidth < self.display_width:
                randNumber = randrange(4)
                imgToUse = grass0Img
                if randNumber == 1:
                    imgToUse = grass1Img
                elif randNumber == 2:
                    imgToUse = grass2Img
                elif randNumber == 3:
                    imgToUse = grass3Img
                self.screen.blit(imgToUse, (currentWidth, currentHeight))
                currentWidth += self.basic_square_size
                SquareDict[(currentWidth, currentHeight)] = 'GRASS'
            currentHeight += self.basic_square_size
            currentWidth = 0

        # adding props to scene
        currentHeight = 0
        currentWidth = 0
        while currentHeight < self.display_height:
            while currentWidth < self.display_width:
                randNumber = randrange(100)
                if 30 >= randNumber > 25: # 5% chance to spawn chicken
                    self.screen.blit(chickenImg, (currentWidth, currentHeight))
                    SquareDict[(currentWidth, currentHeight)] = 'CHICKEN'
                if 40 >= randNumber > 30: # 10% chance to spawn tree
                    self.screen.blit(treeImg, (currentWidth, currentHeight))
                    SquareDict[(currentWidth, currentHeight)] = 'TREE'
                if 50 >= randNumber > 40: # 10% chance to spawn log
                    self.screen.blit(logImg, (currentWidth, currentHeight))
                    SquareDict[(currentWidth, currentHeight)] = 'LOG'
                if 60 >= randNumber > 50: # 10% chance to spawn rock
                    self.screen.blit(rockImg, (currentWidth, currentHeight))
                    SquareDict[(currentWidth, currentHeight)] = 'ROCK'
                currentWidth += self.basic_square_size
            currentHeight += self.basic_square_size
            currentWidth = 0