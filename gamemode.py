import math

import pygame

import background
import car


class GameMode:
    NumberOfCars = 1000
    GenerationsToAcceptConvergence = 10000

    CurrentGeneration = 0
    GameIsRunning = True
    Cars = []
    CurrentBackground = None
    NumberOfMutations = 0
    CurrentTurn = 0
    BestCarsInTurn = []

    NetworkConverged = False
    GenerationsWithoutDnaChange = 0
    BestFitEver = -999
    BestDnaEver = None
    BestKillsEver = 0

    def __init__(self):
        self.ResetVariables()

    def ResetVariables(self):
        self.Cars = []
        self.CurrentBackground = None
        self.CurrentTurn = 0

    def ResetGame(self):
        self.GetBestFiveCars()
        self.InitNewGame()
        self.ChangeCarsDna()

    def GetBestFiveCars(self):
        # Sorting cars by score
        self.Cars.sort(key=lambda x: x.Rewards, reverse=True)
        self.BestCarsInTurn = self.Cars[:5]
        if len(self.BestCarsInTurn) > 0:
            if self.BestCarsInTurn[0].Rewards > self.BestFitEver:
                self.BestFitEver = self.BestCarsInTurn[0].Rewards

    def InitNewGame(self):
        print("---------- Init generation: " + str(self.CurrentGeneration) + " ----------")
        self.ResetVariables()
        self.CurrentBackground = background.Background()
        self.CreateCars()
        self.CurrentGeneration += 1

    def CreateCars(self):
        InitialLoc = (self.CurrentBackground.DisplayWidth / 2, self.CurrentBackground.DisplayHeight / 2)

        for i in range(self.NumberOfCars):
            self.Cars.append(car.Car(InitialLoc, self))

        if self.CurrentGeneration == 0:
            self.NumberOfMutations = len(self.Cars[0].Dna)

    def ChangeCarsDna(self):
        if len(self.BestCarsInTurn) == 0:
            return
        print("Best car score (round): " + str(self.BestCarsInTurn[0].Rewards))
        print("Best car DNA(round): " + str(self.BestCarsInTurn[0].Dna))
        self.CloneBestCars()
        self.MutateCars()
        self.NumberOfMutations *= 0.999
        if self.NumberOfMutations < len(self.Cars[0].Dna) / 3:
            self.NumberOfMutations = len(self.Cars[0].Dna) / 3
        print("Mutating " + str(math.ceil(self.NumberOfMutations)) + " DNAs.")

    def CloneBestCars(self):
        for i in range(len(self.Cars)):
            if i < len(self.BestCarsInTurn):
                self.Cars[i].Dna = self.BestCarsInTurn[i].Dna

    def MutateCars(self):
        for i in range(len(self.BestCarsInTurn), len(self.Cars)):
            self.Cars[i].MutateDna(self.NumberOfMutations)

    def OnTurnEnd(self):
        if self.CheckIfGameOver():
            print("Game over in turn: " + str(self.CurrentTurn))
            self.ResetGame()
            return
        self.CurrentTurn += 1

    def CheckIfGameOver(self):
        for CurrentCar in self.Cars:
            if CurrentCar.IsDead:
                continue
            return False
        return True

    def DrawBestFitness(self, initial_x_loc, initial_y_loc):
        if self.CurrentBackground.Screen is None:
            return

        Font = pygame.font.SysFont("comicsansms", 13)
        BestFitText = Font.render("Best fitness (round): " + str(self.BestCarsInTurn[0].Rewards), True, (0, 0, 0))
        BestFitEverText = Font.render("Best fitness (ever): " + str(self.BestFitEver), True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(BestFitEverText, (initial_x_loc, initial_y_loc))
        self.CurrentBackground.Screen.blit(BestFitText, (initial_x_loc, initial_y_loc + 15))

    def DrawCurrentGeneration(self, initial_x_loc, initial_y_loc):
        Font = pygame.font.SysFont("comicsansms", 14)
        CurrentGenerationText = Font.render("Generation: " + str(self.CurrentGeneration), True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(CurrentGenerationText, (initial_x_loc, initial_y_loc))

    def DrawNeuralNet(self, initial_x_loc, initial_y_loc):
        BIAS = 1
        EachNeuronOffset = 20
        if self.BestCarsInTurn[0] is None:
            return

        BestCharacterBrain = self.BestCarsInTurn[0].Brain

        # Drawing first layer texts
        Font = pygame.font.SysFont("comicsansms", 14)
        FirstNeuronText = Font.render("XDist", True, (0, 0, 0))
        SecondNeuronText = Font.render("Equal", True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(FirstNeuronText, (initial_x_loc, initial_y_loc - 13))
        self.CurrentBackground.Screen.blit(SecondNeuronText, (initial_x_loc, 20 + initial_y_loc - 13))

        # Drawing first layer neurons
        for i in range(len(BestCharacterBrain.EntryLayer.Neurons) - BIAS):
            NeuronColor = (0, 0, 0) if BestCharacterBrain.EntryLayer.Neurons[i].OutValue == 0 else (255, 0, 0)
            pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor,
                               (initial_x_loc + 50, initial_y_loc + i * EachNeuronOffset),
                               7)

        # Drawing hidden layers neurons
        for i in range(len(BestCharacterBrain.HiddenLayers)):
            for j in range(len(BestCharacterBrain.HiddenLayers[i].Neurons) - BIAS):
                NeuronColor = (0, 0, 0) if BestCharacterBrain.HiddenLayers[i].Neurons[j].OutValue == 0 else (255, 0, 0)
                pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor,
                                   (initial_x_loc + 100 + i * 50, initial_y_loc + j * EachNeuronOffset),
                                   7)

        # Drawing output layer neurons
        for i in range(len(BestCharacterBrain.LastCalculatedOutput)):
            NeuronColor = (0, 0, 0) if BestCharacterBrain.LastCalculatedOutput[i] == 0 else (255, 0, 0)
            pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor,
                               (initial_x_loc + 150, initial_y_loc + i * EachNeuronOffset),
                               7)

        # Drawing output layer texts
        FirstNeuronText = Font.render("Left", True, (0, 0, 0))
        SecondNeuronText = Font.render("Right", True, (0, 0, 0))
        ThirdNeuronText = Font.render("Nothing", True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(FirstNeuronText, (initial_x_loc + 160, initial_y_loc - 13))
        self.CurrentBackground.Screen.blit(SecondNeuronText,
                                           (initial_x_loc + 160, initial_y_loc + 1 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(ThirdNeuronText,
                                           (initial_x_loc + 160, initial_y_loc + 2 * EachNeuronOffset - 13))

        # Drawing connections
        for i in range(len(BestCharacterBrain.EntryLayer.Neurons) - BIAS):
            for j in range(len(BestCharacterBrain.HiddenLayers[0].Neurons) - BIAS):
                if BestCharacterBrain.EntryLayer.Neurons[i].OutValue > 0 and BestCharacterBrain.HiddenLayers[0].Neurons[
                    j].OutValue > 0:
                    pygame.draw.line(self.CurrentBackground.Screen, (255, 0, 0),
                                     (initial_x_loc + 50, initial_y_loc + i * EachNeuronOffset),
                                     (initial_x_loc + 100, initial_y_loc + j * EachNeuronOffset), 1)
                else:
                    pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0),
                                     (initial_x_loc + 50, initial_y_loc + i * EachNeuronOffset),
                                     (initial_x_loc + 100, initial_y_loc + j * EachNeuronOffset), 1)
        if len(BestCharacterBrain.HiddenLayers) > 1:
            for i in range(len(BestCharacterBrain.HiddenLayers[0].Neurons) - BIAS):
                for j in range(len(BestCharacterBrain.HiddenLayers[1].Neurons) - BIAS):
                    if BestCharacterBrain.HiddenLayers[0].Neurons[i].OutValue > 0:
                        pygame.draw.line(self.CurrentBackground.Screen, (255, 0, 0),
                                         (initial_x_loc + 100, initial_y_loc + i * EachNeuronOffset),
                                         (initial_x_loc + 150, initial_y_loc + j * EachNeuronOffset), 1)
                    else:
                        pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0),
                                         (initial_x_loc + 100, initial_y_loc + i * EachNeuronOffset),
                                         (initial_x_loc + 150, initial_y_loc + j * EachNeuronOffset), 1)
        for i in range(len(BestCharacterBrain.HiddenLayers[-1].Neurons) - BIAS):
            for j in range(len(BestCharacterBrain.LastCalculatedOutput)):
                if BestCharacterBrain.HiddenLayers[-1].Neurons[i].OutValue > 0 and \
                        BestCharacterBrain.LastCalculatedOutput[j] != 0:
                    pygame.draw.line(self.CurrentBackground.Screen, (255, 0, 0),
                                     (initial_x_loc + 100, initial_y_loc + i * EachNeuronOffset),
                                     (initial_x_loc + 150, initial_y_loc + j * EachNeuronOffset), 1)
                else:
                    pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0),
                                     (initial_x_loc + 100, initial_y_loc + i * EachNeuronOffset),
                                     (initial_x_loc + 150, initial_y_loc + j * EachNeuronOffset), 1)

    def DrawBestCharacterIndex(self, initial_x_loc, initial_y_loc):
        BestCharacterIndex = self.Cars.index(self.BestCarsInTurn[0])
        Font = pygame.font.SysFont("comicsansms", 14)
        CurrentKillsText = Font.render("Best Character Index: " + str(BestCharacterIndex), True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(CurrentKillsText, (initial_x_loc, initial_y_loc))

    def DrawInfo(self):
        InitialYLoc = 0
        InitialXLoc = self.CurrentBackground.DisplayWidth
        pygame.draw.rect(self.CurrentBackground.Screen, (255, 255, 255), (InitialXLoc, InitialYLoc, 275, 300))

        self.DrawCurrentGeneration(InitialXLoc, InitialYLoc)
        self.GetBestFiveCars()
        self.DrawBestFitness(InitialXLoc, InitialYLoc + 15)
        self.DrawBestCharacterIndex(InitialXLoc, InitialYLoc + 45)
        self.DrawNeuralNet(InitialXLoc, InitialYLoc + 105)
