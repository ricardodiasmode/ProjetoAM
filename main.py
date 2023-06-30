import time
import pygame
import gamemode

# LINK PARA O VÍDEO NO YOUTUBE: https://youtu.be/RVlLLstpe1Q

# Basic game setups
pygame.init()
Clock = pygame.time.Clock()
GameMode = gamemode.GameMode()
GameMode.ResetGame()
pygame.display.update()
ShouldDrawInfo = False
SleepTime = 0.0

while GameMode.GameIsRunning:
    # Event loop
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            GameMode.GameIsRunning = False
        if Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_s:
                ShouldDrawInfo = not ShouldDrawInfo
            elif Event.key == pygame.K_DOWN:
                SleepTime += 0.01
            elif Event.key == pygame.K_UP:
                SleepTime -= 0.01
                if SleepTime < 0:
                    SleepTime = 0

    GameMode.CurrentBackground.DrawBackground()

    # Game loop
    CurrentAliveCars = 0
    for CurrentCar in GameMode.Cars:
        if GameMode.CurrentBackground.SquareDict[CurrentCar.CurrentLocation] == "LOG":
            CurrentCar.Die()
        if CurrentCar.IsDead:
            continue
        CurrentCar.Brain.Think(CurrentCar, GameMode)
        CurrentCar.React()
        CurrentAliveCars += 1
    print("Turn: " + str(GameMode.CurrentTurn) + " | Alive cars: " + CurrentAliveCars.__str__())

    if ShouldDrawInfo:
        GameMode.DrawInfo()  # This slow down the game a lot
    time.sleep(SleepTime)

    GameMode.OnTurnEnd()

    # Update loop
    pygame.display.update()
    Clock.tick()
