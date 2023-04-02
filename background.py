import pygame
from random import randrange
from enum import Enum


class Background:
    SquareType = Enum('SquareType', ['GRASS', 'LOG', 'TREE', 'ROCK', 'TENT', 'CHICKEN', 'RIVER'])
    square_image_dict = {}

    # filling background with grass
    square_dict = {
        (0, 0): 'GRASS'
    }

    grass0Img = pygame.image.load('Grass0.png')
    grass1Img = pygame.image.load('Grass1.png')
    grass2Img = pygame.image.load('Grass2.png')
    grass3Img = pygame.image.load('Grass3.png')

    display_width = 1280
    display_height = 720
    basic_square_size = 64
    screen = None

    def __init__(self):
        self.screen = pygame.display.set_mode((self.display_width, self.display_height + 50))

    def drawBackground(self):
        # loading images
        chickenImg = pygame.image.load('Galinha.png')
        treeImg = pygame.image.load('Tree.png')
        logImg = pygame.image.load('Log.png')
        rockImg = pygame.image.load('Rock.png')

        currentHeight = 0
        currentWidth = 0
        while currentHeight < self.display_height:
            while currentWidth < self.display_width:
                randNumber = randrange(4)
                imgToUse = self.grass0Img
                if randNumber == 1:
                    imgToUse = self.grass1Img
                elif randNumber == 2:
                    imgToUse = self.grass2Img
                elif randNumber == 3:
                    imgToUse = self.grass3Img
                self.screen.blit(imgToUse, (currentWidth, currentHeight))
                self.square_image_dict[(currentWidth, currentHeight)] = imgToUse
                self.square_dict[(currentWidth, currentHeight)] = 'GRASS'
                currentWidth += self.basic_square_size
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
                    self.square_image_dict[(currentWidth, currentHeight)] = chickenImg
                    self.square_dict[(currentWidth, currentHeight)] = 'CHICKEN'
                if 40 >= randNumber > 30: # 10% chance to spawn tree
                    self.screen.blit(treeImg, (currentWidth, currentHeight))
                    self.square_image_dict[(currentWidth, currentHeight)] = treeImg
                    self.square_dict[(currentWidth, currentHeight)] = 'TREE'
                if 50 >= randNumber > 40: # 10% chance to spawn log
                    self.screen.blit(logImg, (currentWidth, currentHeight))
                    self.square_image_dict[(currentWidth, currentHeight)] = logImg
                    self.square_dict[(currentWidth, currentHeight)] = 'LOG'
                if 60 >= randNumber > 50: # 10% chance to spawn rock
                    self.screen.blit(rockImg, (currentWidth, currentHeight))
                    self.square_image_dict[(currentWidth, currentHeight)] = rockImg
                    self.square_dict[(currentWidth, currentHeight)] = 'ROCK'
                currentWidth += self.basic_square_size
            currentHeight += self.basic_square_size
            currentWidth = 0