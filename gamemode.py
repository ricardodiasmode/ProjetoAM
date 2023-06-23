import background
import character


class GameMode:
    NumberOfCharactersEachTeam = 10
    CurrentGeneration = 0
    GameIsRunning = True
    Characters = []
    CurrentBackground = None
    BestDna = None
    NumberOfMutations = 0
    CurrentTurn = 0

    def __init__(self):
        self.ResetVariables()

    def ResetVariables(self):
        self.Characters = []
        self.CurrentBackground = None
        self.CurrentTurn = 0

    def ResetGame(self):
        self.InitNewGame()
        self.MutateCharacters()

    def GetBestTwoCharacters(self):
        BestCharacter = None
        SecondBestCharacter = None
        for CurrentCharacter in self.Characters:
            if BestCharacter is None:
                BestCharacter = CurrentCharacter
            elif CurrentCharacter.Score > BestCharacter.Score:
                SecondBestCharacter = BestCharacter
                BestCharacter = CurrentCharacter
            elif SecondBestCharacter is None or CurrentCharacter.Score > SecondBestCharacter.Score:
                SecondBestCharacter = CurrentCharacter

        return BestCharacter, SecondBestCharacter

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
        BestCharacter, SecondBestCharacter = self.GetBestTwoCharacters()
        self.BestDna = BestCharacter.Dna
        print("Best DNA: " + str(self.BestDna))

        self.CloneBestTwoCharacters(BestCharacter, SecondBestCharacter)

        self.MutateNotClonedCharacters()
        self.NumberOfMutations *= 0.999

    def CloneBestTwoCharacters(self, best_character, second_best_character):
        for i in range(len(self.Characters)):
            if i % 2 == 0:
                continue
            if i % 3 == 0:
                self.Characters[i].Dna = second_best_character.Dna
            else:
                self.Characters[i].Dna = best_character.Dna

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
