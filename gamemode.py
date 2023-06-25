import math
import time

import pygame

import background
import character


class GameMode:
    NumberOfCharactersEachTeam = 10
    CurrentGeneration = 0
    GameIsRunning = True
    Characters = []
    CurrentBackground = None
    NumberOfMutations = 0
    CurrentTurn = 0
    SecondBestCharacterDna = None
    BestCharacterDna = None
    BestCharacterScore = -999
    SecondBestCharacterScore = -999
    BestFitEver = -999
    BestCharacterRef = None
    BestCharacterKills = 0

    def __init__(self):
        self.ResetVariables()

    def ResetVariables(self):
        self.Characters = []
        self.CurrentBackground = None
        self.CurrentTurn = 0

    def ResetGame(self):
        self.GetBestTwoCharacters()

        if self.BestCharacterScore > self.BestFitEver:
            self.BestFitEver = self.BestCharacterScore

        self.InitNewGame()
        self.MutateCharacters()

    def GetBestTwoCharacters(self):
        for CurrentCharacter in self.Characters:
            if self.BestCharacterDna is None:
                self.BestCharacterDna = CurrentCharacter.Dna
                self.BestCharacterScore = CurrentCharacter.Score
                self.BestCharacterRef = CurrentCharacter
                self.BestCharacterKills = CurrentCharacter.Kills
            elif CurrentCharacter.Score > self.BestCharacterScore:
                self.SecondBestCharacterDna = self.BestCharacterDna
                self.SecondBestCharacterScore = self.BestCharacterScore
                self.BestCharacterScore = CurrentCharacter.Score
                self.BestCharacterDna = CurrentCharacter.Dna
                self.BestCharacterRef = CurrentCharacter
                self.BestCharacterKills = CurrentCharacter.Kills
            elif self.SecondBestCharacterDna is None or CurrentCharacter.Score >= self.SecondBestCharacterScore:
                self.SecondBestCharacterDna = CurrentCharacter.Dna
                self.SecondBestCharacterScore = CurrentCharacter.Score
            # updating score
            if self.BestCharacterDna == CurrentCharacter.Dna:
                self.BestCharacterScore = CurrentCharacter.Score
                self.BestCharacterRef = CurrentCharacter
            if self.SecondBestCharacterDna == CurrentCharacter.Dna:
                self.SecondBestCharacterScore = CurrentCharacter.Score

    def InitNewGame(self):
        print("Init generation: " + str(self.CurrentGeneration))
        self.ResetVariables()
        self.CurrentBackground = background.Background()
        self.CreateCharacters()
        self.CurrentGeneration += 1

    def CreateCharacters(self):
        InitialBlueTeamPos = (self.CurrentBackground.DisplayWidth / 4, 0)
        InitialRedTeamPos = (InitialBlueTeamPos[0] * 3, 0)

        for i in range(self.NumberOfCharactersEachTeam):
            CurrentBlueTeamPos = (InitialBlueTeamPos[0], InitialBlueTeamPos[1] + i * 64)
            CurrentRedTeamPos = (InitialRedTeamPos[0], InitialRedTeamPos[1] + i * 64)
            self.Characters.append(character.Character(True, CurrentBlueTeamPos, self))
            self.Characters.append(character.Character(False, CurrentRedTeamPos, self))

        if self.CurrentGeneration == 0:
            self.NumberOfMutations = len(self.Characters[0].Dna)

    def MutateCharacters(self):
        if self.BestCharacterDna is None:
            return

        print("Best DNA: " + str(self.BestCharacterDna))
        print("Best character score: " + str(self.BestCharacterScore))
        print("Best character kills: " + str(self.BestCharacterKills))

        self.CloneBestTwoCharacters()

        if self.NumberOfMutations > 1:
            self.MutateNotClonedCharacters()
            self.NumberOfMutations *= 0.99
            print("Mutating " + str(math.ceil(self.NumberOfMutations)) + " DNAs.")
        else:
            print("Network converged. No mutations will occur.")

    def CloneBestTwoCharacters(self):
        for i in range(len(self.Characters)):
            if i % 2 == 0:
                continue
            if i % 3 == 0:
                self.Characters[i].Dna = self.SecondBestCharacterDna
            else:
                self.Characters[i].Dna = self.BestCharacterDna

    def MutateNotClonedCharacters(self):
        for i in range(len(self.Characters)):
            if i % 2 == 0:
                self.Characters[i].MutateDna(self.NumberOfMutations)

    def OnTurnEnd(self):
        if self.CheckIfGameOver():
            print("Game over in turn: " + str(self.CurrentTurn))
            self.ResetGame()
        self.CurrentTurn += 1

    def CheckIfGameOver(self):
        FoundBlueTeam = False
        FoundRedTeam = False
        for CurrentCharacter in self.Characters:
            if CurrentCharacter.IsDead:
                continue
            if CurrentCharacter.BlueTeamMember:
                FoundBlueTeam = True
            else:
                FoundRedTeam = True
        return not FoundBlueTeam or not FoundRedTeam

    def HasAnyCharacterHere(self, position):
        for CurrentCharacter in self.Characters:
            if CurrentCharacter.IsDead:
                continue
            if CurrentCharacter.CurrentLocation == position:
                return True
        return False

    def DrawBestFitness(self, initial_y_loc):
        if self.BestCharacterRef.Score == -999:
            return
        if self.CurrentBackground.Screen is None:
            return

        Font = pygame.font.SysFont("comicsansms", 13)
        BestFitText = Font.render("Best fitness (round): " + str(self.BestCharacterRef.Score), True, (0, 0, 0))
        BestFitEverText = Font.render("Best fitness (ever): " + str(self.BestFitEver), True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(BestFitEverText, (50, initial_y_loc))
        self.CurrentBackground.Screen.blit(BestFitText, (50, initial_y_loc + 15))

    def DrawCurrentGeneration(self, initial_y_loc):
        Font = pygame.font.SysFont("comicsansms", 14)
        CurrentGenerationText = Font.render("Generation: " + str(self.CurrentGeneration), True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(CurrentGenerationText, (50, initial_y_loc))

    def DrawNeuralNet(self, initial_y_loc):
        BIAS = 1
        EachNeuronOffset = 20
        if self.BestCharacterRef is None:
            return

        BestCharacterBrain = self.BestCharacterRef.Brain

        # Drawing first layer texts
        Font = pygame.font.SysFont("comicsansms", 14)
        FirstNeuronText = Font.render("XLog", True, (0, 0, 0))
        SecondNeuronText = Font.render("YLog", True, (0, 0, 0))
        ThirdNeuronText = Font.render("HasLog", True, (0, 0, 0))
        ForthNeuronText = Font.render("HasKnife", True, (0, 0, 0))
        FifthNeuronText = Font.render("XEnemy", True, (0, 0, 0))
        SixNeuronText = Font.render("YEnemy", True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(FirstNeuronText, (50, initial_y_loc - 13))
        self.CurrentBackground.Screen.blit(SecondNeuronText, (50, initial_y_loc + 1 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(ThirdNeuronText, (50, initial_y_loc + 2 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(ForthNeuronText, (50, initial_y_loc + 3 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(FifthNeuronText, (50, initial_y_loc + 4 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(SixNeuronText, (50, initial_y_loc + 5 * EachNeuronOffset - 13))

        # Drawing first layer neurons
        for i in range(len(BestCharacterBrain.EntryLayer.Neurons) - BIAS):
            NeuronColor = (0, 0, 0) if BestCharacterBrain.EntryLayer.Neurons[i].OutValue == 0 else (255, 0, 0)
            NextLayerOffset = EachNeuronOffset
            pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor, (100, initial_y_loc + i * EachNeuronOffset), 7)

        # Drawing hidden layers neurons
        for i in range(len(BestCharacterBrain.HiddenLayers)):
            for j in range(len(BestCharacterBrain.HiddenLayers[i].Neurons) - BIAS):
                NeuronColor = (0, 0, 0) if BestCharacterBrain.HiddenLayers[i].Neurons[j].OutValue == 0 else (255, 0, 0)
                pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor, (150 + i * 50, initial_y_loc + j * EachNeuronOffset),
                                   7)

        # Drawing output layer neurons
        for i in range(len(BestCharacterBrain.LastCalculatedOutput)):
            NeuronColor = (0, 0, 0) if BestCharacterBrain.LastCalculatedOutput[i] == 0 else (255, 0, 0)
            pygame.draw.circle(self.CurrentBackground.Screen, NeuronColor, (200, initial_y_loc + i * EachNeuronOffset),
                               7)

        # Drawing output layer texts
        FirstNeuronText = Font.render("MoveToLog", True, (0, 0, 0))
        SecondNeuronText = Font.render("MoveToEnemy", True, (0, 0, 0))
        ThirdNeuronText = Font.render("Pickup", True, (0, 0, 0))
        FourthNeuronText = Font.render("CraftKnife", True, (0, 0, 0))
        FifthNeuronText = Font.render("Attack", True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(FirstNeuronText, (210, initial_y_loc - 13))
        self.CurrentBackground.Screen.blit(SecondNeuronText, (210, initial_y_loc + 1 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(ThirdNeuronText, (210, initial_y_loc + 2 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(FourthNeuronText, (210, initial_y_loc + 3 * EachNeuronOffset - 13))
        self.CurrentBackground.Screen.blit(FifthNeuronText, (210, initial_y_loc + 4 * EachNeuronOffset - 13))

        # Drawing connections
        for i in range(len(BestCharacterBrain.EntryLayer.Neurons) - BIAS):
            for j in range(len(BestCharacterBrain.HiddenLayers[0].Neurons) - BIAS):
                if BestCharacterBrain.EntryLayer.Neurons[i].OutValue > 0 and BestCharacterBrain.HiddenLayers[0].Neurons[j].OutValue > 0:
                    pygame.draw.line(self.CurrentBackground.Screen, (255, 0, 0), (100, initial_y_loc + i * EachNeuronOffset),
                                     (150, initial_y_loc + j * EachNeuronOffset), 1)
                else:
                    pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0), (100, initial_y_loc + i * EachNeuronOffset),
                                     (150, initial_y_loc + j * EachNeuronOffset), 1)
        if len(BestCharacterBrain.HiddenLayers) > 1:
            for i in range(len(BestCharacterBrain.HiddenLayers[0].Neurons) - BIAS):
                for j in range(len(BestCharacterBrain.HiddenLayers[1].Neurons) - BIAS):
                    if BestCharacterBrain.HiddenLayers[0].Neurons[i].OutValue > 0:
                        pygame.draw.line(self.CurrentBackground.Screen, (255, 0, 0), (150, initial_y_loc + i * EachNeuronOffset),
                                         (200, initial_y_loc + j * EachNeuronOffset), 1)
                    else:
                        pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0), (150, initial_y_loc + i * EachNeuronOffset),
                                         (200, initial_y_loc + j * EachNeuronOffset), 1)
        for i in range(len(BestCharacterBrain.HiddenLayers[-1].Neurons) - BIAS):
            for j in range(len(BestCharacterBrain.LastCalculatedOutput)):
                if BestCharacterBrain.HiddenLayers[-1].Neurons[i].OutValue > 0 and BestCharacterBrain.LastCalculatedOutput[j] != 0:
                    pygame.draw.line(self.CurrentBackground.Screen, (255, 0, 0), (150, initial_y_loc + i * EachNeuronOffset),
                                     (200, initial_y_loc + j * EachNeuronOffset), 1)
                else:
                    pygame.draw.line(self.CurrentBackground.Screen, (0, 0, 0), (150, initial_y_loc + i * EachNeuronOffset),
                                     (200, initial_y_loc + j * EachNeuronOffset), 1)

    def DrawBestCharacterCurrentKills(self, initial_y_loc):
        Font = pygame.font.SysFont("comicsansms", 14)
        CurrentKillsText = Font.render("Best Character Kills: " + str(self.BestCharacterRef.Kills), True, (0, 0, 0))
        self.CurrentBackground.Screen.blit(CurrentKillsText, (50, initial_y_loc))


    def DrawInfo(self):
        InitialYLoc = 50
        pygame.draw.rect(self.CurrentBackground.Screen, (255, 255, 255), (50, InitialYLoc, 250, 200))

        self.DrawCurrentGeneration(InitialYLoc)
        self.GetBestTwoCharacters()
        self.DrawBestFitness(InitialYLoc + 15)
        self.DrawBestCharacterCurrentKills(InitialYLoc + 45)
        self.DrawNeuralNet(InitialYLoc + 75)
