import random
from math import ceil

import pygame

import neuralNetwork


class Character:
    CurrentLocation = (0, 0)
    PlayerImage = None
    GameMode = None
    HasLog = False
    HasKnife = False
    BlueTeamMember = False
    Energy = 100
    IsDead = False
    Brain = None
    Dna = []
    Score = 0

    def __init__(self, blue_team, location, game_mode):
        self.CurrentLocation = location
        self.GameMode = game_mode
        self.BlueTeamMember = blue_team
        self.UpdateImage()

        # initializing neural network
        self.Brain = neuralNetwork.NeuralNetwork()
        self.Dna = []
        for i in range(self.Brain.GetWeightAmount()):
            self.Dna.append((random.randint(0, 20000) / 10.0) - 1000.0)

        if game_mode.CurrentBackground.SquareDict[self.CurrentLocation] == "LOG":
            self.RemoveItemOnGround("LOG")

    def UpdateImage(self):
        PlayerTeamName = "Blue" if self.BlueTeamMember else "Red"
        PlayerObjectName = ""
        if self.HasLog:
            PlayerObjectName = "WithLog"
        elif self.HasKnife:
            PlayerObjectName = "WithKnife"

        self.PlayerImage = pygame.image.load(PlayerTeamName + "Character" + PlayerObjectName + ".png")

    def RemoveItemOnGround(self, item):
        if item == "LOG":
            CurrentBackground = self.GameMode.CurrentBackground
            CurrentBackground.Screen.blit(self.PlayerImage, self.CurrentLocation)
            CurrentBackground.SquareDict[self.CurrentLocation] = "GRASS"
            CurrentBackground.SquareImageDict[self.CurrentLocation] = CurrentBackground.Grass1Img
            CurrentBackground.LogLocations.remove(self.CurrentLocation)

    def GetAction(self, action_index):
        if action_index == 0:
            self.MoveLeft()
        elif action_index == 1:
            self.MoveRight()
        elif action_index == 2:
            self.MoveUp()
        elif action_index == 3:
            self.MoveDown()
        elif action_index == 4:
            self.PickUp()
        elif action_index == 5:
            self.CraftKnife()

    def React(self):
        # Set a probability to hit the desired action
        ProbabilityToHit = 0.9
        random_number = random.uniform(0, 1)
        OutputLen = len(self.Brain.LastCalculatedOutput)

        for i in range(OutputLen):
            if random_number < ProbabilityToHit and self.Brain.LastCalculatedOutput[i] > 0:
                self.GetAction(i)
                return

        # If no action was hit, take random action
        self.GetAction(random.randint(0, OutputLen-1))

    def CraftKnife(self):
        self.RemoveEnergy()
        self.Score -= 1
        if self.HasLog:
            self.HasLog = False
            self.Score += 30
            self.HasKnife = True
            self.UpdateImage()

    def MoveLeft(self):
        self.Move((-64, 0))

    def MoveRight(self):
        self.Move((64, 0))

    def MoveUp(self):
        self.Move((0, -64))

    def MoveDown(self):
        self.Move((0, 64))

    def Move(self, position):
        self.Score -= 1
        self.RemoveEnergy()
        LocationToGo = (self.CurrentLocation[0] + position[0], self.CurrentLocation[1] + position[1])

        if LocationToGo[0] < 0 or LocationToGo[0] >= self.GameMode.CurrentBackground.DisplayWidth or \
                LocationToGo[1] < 0 or LocationToGo[1] >= self.GameMode.CurrentBackground.DisplayHeight:
            self.RemoveEnergy()
            return

        if self.GameMode.HasAnyCharacterHere(LocationToGo):
            self.RemoveEnergy()
            return

        ImageBelow = self.GameMode.CurrentBackground.SquareImageDict[self.CurrentLocation]
        self.GameMode.CurrentBackground.Screen.blit(ImageBelow, self.CurrentLocation)
        self.GameMode.CurrentBackground.Screen.blit(self.PlayerImage, LocationToGo)
        self.CurrentLocation = LocationToGo

    def RemoveEnergy(self):
        self.Energy -= 1
        if self.Energy <= 0:
            self.IsDead = True
            ImageBelow = self.GameMode.CurrentBackground.SquareImageDict[self.CurrentLocation]
            self.GameMode.CurrentBackground.Screen.blit(ImageBelow, self.CurrentLocation)

    def PickUp(self):
        self.RemoveEnergy()
        self.Score -= 1
        if self.HasLog or self.HasKnife:
            self.Score -= 1
            return

        if self.GameMode.CurrentBackground.SquareDict[self.CurrentLocation] == "LOG":
            self.HasLog = True
            self.UpdateImage()
            self.RemoveItemOnGround("LOG")
            self.Score += 16

    def MutateDna(self, number_of_mutations):
        for i in range(ceil(number_of_mutations)):
            MutationType = random.randint(0, 2)
            IndexToMutate = random.randint(0, len(self.Dna) - 1)
            if MutationType == 0:
                self.Dna[IndexToMutate] = ((random.randint(0, 20000) / 10.0) - 1000.0)
            elif MutationType == 1:
                self.Dna[IndexToMutate] *= ((random.randint(0, 10000) / 10000.0) + 0.5)
            elif MutationType == 2:
                self.Dna[IndexToMutate] += (((random.randint(0, 20000) / 10.0) - 1000.0) / 100.0)
