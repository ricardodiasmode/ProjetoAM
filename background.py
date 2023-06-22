import pygame
from random import randrange
from enum import Enum

import utils


class Background:
    SquareType = Enum('SquareType', ['GRASS', 'LOG'])
    square_image_dict = {}

    # filling background with grass
    square_dict = {
        (0, 0): 'GRASS'
    }

    logs_location = []

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
        self.rocks_location = []
        self.logs_location = []
        self.square_image_dict = {}
        self.square_dict = {
            (0, 0): 'GRASS'
        }

    def drawBackground(self):
        # loading images
        logImg = pygame.image.load('Log.png')

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
                if 40 >= randNumber > 20:  # 20% chance to spawn log
                    self.screen.blit(logImg, (currentWidth, currentHeight))
                    self.square_image_dict[(currentWidth, currentHeight)] = logImg
                    self.square_dict[(currentWidth, currentHeight)] = 'LOG'
                    self.logs_location.append((currentWidth, currentHeight))
                currentWidth += self.basic_square_size
            currentHeight += self.basic_square_size
            currentWidth = 0

    def remove_log_of_location(self, location):
        if utils.any_location_equal(location, self.logs_location):
            print("removing log from location: " + str(location))
            self.logs_location.remove(location)

        self.square_dict[location] = 'GRASS'
        self.square_image_dict[location] = self.grass0Img
        self.screen.blit(self.grass0Img, location)

