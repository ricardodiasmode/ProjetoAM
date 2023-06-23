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

    def __init__(self):
        self.ResetVariables()

    def ResetVariables(self):
        self.Characters = []
        self.CurrentBackground = None
        self.CurrentTurn = 0

    def ResetGame(self):
        self.BestCharacterDna = None
        self.BestCharacterScore = -999
        self.SecondBestCharacterDna = None
        self.SecondBestCharacterScore = -999

        self.GetBestTwoCharacters()
        self.InitNewGame()
        self.MutateCharacters()

    def GetBestTwoCharacters(self):
        for CurrentCharacter in self.Characters:
            if self.BestCharacterDna is None:
                self.BestCharacterDna = CurrentCharacter.Dna
            elif CurrentCharacter.Score > self.BestCharacterScore:
                self.SecondBestCharacterDna = self.BestCharacterDna
                self.SecondBestCharacterScore = self.BestCharacterScore

                self.BestCharacterScore = CurrentCharacter.Score
                self.BestCharacterDna = CurrentCharacter.Dna
            elif self.SecondBestCharacterDna is None or CurrentCharacter.Score >= self.SecondBestCharacterScore:
                self.SecondBestCharacterDna = CurrentCharacter.Dna
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
            print("WTF!")
            return

        print("Best DNA: " + str(self.BestCharacterDna))
        print("Best character score: " + str(self.BestCharacterScore))

        self.CloneBestTwoCharacters()

        self.MutateNotClonedCharacters()
        self.NumberOfMutations *= 0.999

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
