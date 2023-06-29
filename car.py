import math
import random
import pygame
import neuralNetwork

BASE_REWARD = 100


class Car:
    CurrentLocation = (0, 0)
    PlayerImage = None
    GameMode = None
    IsDead = False
    Brain = None
    Dna = []
    Rewards = 0

    def __init__(self, location, game_mode):
        self.CurrentLocation = location
        self.GameMode = game_mode
        self.UpdateImage()
        # initializing neural network
        self.Brain = neuralNetwork.NeuralNetwork()
        self.Dna = []
        for i in range(self.Brain.GetWeightAmount()):
            self.Dna.append((random.randint(0, 20000) / 10.0) - 1000.0)

    def UpdateImage(self):
        self.PlayerImage = pygame.image.load("car.png")
        ImageBelow = self.GameMode.CurrentBackground.SquareImageDict[self.CurrentLocation]
        self.GameMode.CurrentBackground.Screen.blit(ImageBelow, self.CurrentLocation)
        self.GameMode.CurrentBackground.Screen.blit(self.PlayerImage, self.CurrentLocation)

    def React(self):
        OutputLen = len(self.Brain.LastCalculatedOutput)
        for i in range(OutputLen):
            if self.Brain.LastCalculatedOutput[i] > 0:
                self.GetAction(i)
                return
        self.GetAction(-1)

    def MoveLeft(self):
        self.Move((-64, 0))

    def MoveRight(self):
        self.Move((64, 0))

    def Move(self, position):
        LocationToGo = (self.CurrentLocation[0] + position[0], self.CurrentLocation[1] + position[1])

        if LocationToGo[0] < 0 or LocationToGo[0] >= self.GameMode.CurrentBackground.DisplayWidth or \
                LocationToGo[1] < 0 or LocationToGo[1] >= self.GameMode.CurrentBackground.DisplayHeight:
            self.GameMode.CurrentBackground.Screen.blit(self.PlayerImage, self.CurrentLocation)
            return

        self.CurrentLocation = LocationToGo
        self.GameMode.CurrentBackground.Screen.blit(self.PlayerImage, self.CurrentLocation)

    def Die(self):
        self.IsDead = True

    def MutateDna(self, number_of_mutations):
        for k in range(math.ceil(number_of_mutations)):
            in_type = random.randint(0, 2)
            index = random.randint(0, len(self.Dna) - 1)
            if in_type == 0:
                self.Dna[index] = (random.randint(0, 20000) / 10.0) - 1000.0
            elif in_type == 1:
                number = (random.randint(0, 10000) / 10000.0) + 0.5
                self.Dna[index] *= self.Dna[index] * number
            elif in_type == 2:
                number = (random.randint(0, 20000) / 10.0) - 1000.0 / 100.0
                self.Dna[index] += self.Dna[index] + number

    def GetAction(self, action_index):
        self.Rewards += 1
        if action_index == 0:
            self.MoveLeft()
        elif action_index == 1:
            self.MoveRight()
        else:
            #  Do nothing
            self.GameMode.CurrentBackground.Screen.blit(self.PlayerImage, self.CurrentLocation)
