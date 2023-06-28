import math
import random
from math import ceil
import pygame
import neuralNetwork
import utils

BASE_REWARD = 100
LOG_REWARD_MULTIPLIER = 1
CRAFT_REWARD_MULTIPLIER = 3
KILL_REWARD_MULTIPLIER = 10


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
    ClosestEnemy = None
    ClosestLogLocation = []
    Kills = 0

    def __init__(self, blue_team, location, game_mode):
        self.CurrentLocation = location
        self.GameMode = game_mode
        self.BlueTeamMember = blue_team
        self.UpdateImage()
        self.ClosestEnemy = None
        # initializing neural network
        self.Brain = neuralNetwork.NeuralNetwork()
        self.Dna = []
        for i in range(self.Brain.GetWeightAmount()):
            self.Dna.append((random.randint(0, 20000) / 10.0) - 1000.0)


    def UpdateImage(self):
        PlayerTeamName = "Blue" if self.BlueTeamMember else "Red"
        PlayerObjectName = ""
        if self.HasLog:
            PlayerObjectName = "WithLog"
        elif self.HasKnife:
            PlayerObjectName = "WithKnife"
        if self.IsDead:
            if self.Energy <= 0:
                PlayerObjectName = "EnergyDeath"
            else:
                PlayerObjectName = "Death"
        self.PlayerImage = pygame.image.load(PlayerTeamName + "Character" + PlayerObjectName + ".png")
        ImageBelow = self.GameMode.CurrentBackground.SquareImageDict[self.CurrentLocation]
        self.GameMode.CurrentBackground.Screen.blit(ImageBelow, self.CurrentLocation)
        self.GameMode.CurrentBackground.Screen.blit(self.PlayerImage, self.CurrentLocation)

    def RemoveItemOnGround(self, item):
        if item == "LOG":
            CurrentBackground = self.GameMode.CurrentBackground
            CurrentBackground.Screen.blit(self.PlayerImage, self.CurrentLocation)
            CurrentBackground.SquareDict[self.CurrentLocation] = "GRASS"
            CurrentBackground.SquareImageDict[self.CurrentLocation] = CurrentBackground.Grass1Img
            CurrentBackground.LogLocations.remove(self.CurrentLocation)

    def React(self):
        OutputLen = len(self.Brain.LastCalculatedOutput)
        for i in range(OutputLen):
            if self.Brain.LastCalculatedOutput[i] > 0:
                self.GetAction(i)
                return

    def Attack(self):
        self.RemoveEnergy()
        if utils.DistanceBetweenLocations(self.ClosestEnemy.CurrentLocation, self.CurrentLocation) <= 64 and \
                self.HasKnife:
            self.Score += BASE_REWARD * KILL_REWARD_MULTIPLIER
            self.ClosestEnemy.Die()
            self.Kills += 1

    def CraftKnife(self):
        self.RemoveEnergy()
        if self.HasLog and not self.HasKnife:
            self.HasLog = False
            self.Score += BASE_REWARD * CRAFT_REWARD_MULTIPLIER
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

    def MoveToLog(self):
        self.RemoveEnergy()
        if self.CurrentLocation[0] - self.ClosestLogLocation[0] > 0:
            self.MoveLeft()
        elif self.CurrentLocation[0] - self.ClosestLogLocation[0] < 0:
            self.MoveRight()
        elif self.CurrentLocation[1] - self.ClosestLogLocation[1] > 0:
            self.MoveUp()
        elif self.CurrentLocation[1] - self.ClosestLogLocation[1] < 0:
            self.MoveDown()

    def MoveToEnemy(self):
        self.RemoveEnergy()
        if self.CurrentLocation[0] - self.ClosestEnemy.CurrentLocation[0] > 0:
            self.MoveLeft()
        elif self.CurrentLocation[0] - self.ClosestEnemy.CurrentLocation[0] < 0:
            self.MoveRight()
        elif self.CurrentLocation[1] - self.ClosestEnemy.CurrentLocation[1] > 0:
            self.MoveUp()
        elif self.CurrentLocation[1] - self.ClosestEnemy.CurrentLocation[1] < 0:
            self.MoveDown()

    def RemoveEnergy(self):
        self.Energy -= 1
        if self.Energy <= 0:
            self.Die()

    def Die(self):
        self.IsDead = True
        self.UpdateImage()

    def PickUp(self):
        self.RemoveEnergy()
        if self.HasLog or self.HasKnife:
            return
        if self.GameMode.CurrentBackground.SquareDict[self.CurrentLocation] == "LOG":
            self.HasLog = True
            self.UpdateImage()
            self.RemoveItemOnGround("LOG")
            self.Score += BASE_REWARD * LOG_REWARD_MULTIPLIER

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
        if action_index == 0:
            self.MoveToLog()
        elif action_index == 1:
            self.MoveToEnemy()
        elif action_index == 2:
            self.PickUp()
        elif action_index == 3:
            self.CraftKnife()
        elif action_index == 4:
            self.Attack()

    def GetState(self):
        if self.HasKnife:
            return 0  # only State that attack is allowed
        elif not self.HasLog:
            return 1  # only State that pick up is allowed
        elif self.HasLog and not self.HasKnife:
            return 2  # only State that craft knife is allowed
