import time

import pygame
import gamemode

# Basic game setups
pygame.init()
Clock = pygame.time.Clock()
GameMode = gamemode.GameMode()
GameMode.ResetGame()
pygame.display.update()
ShouldDrawInfo = False
SleepTime = 0.1

while GameMode.GameIsRunning:
    # Event loop
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            GameMode.GameIsRunning = False
        if Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_s:
                ShouldDrawInfo = not ShouldDrawInfo
            elif Event.key == pygame.K_UP:
                SleepTime += 0.001
            elif Event.key == pygame.K_DOWN:
                SleepTime -= 0.001
                if SleepTime < 0:
                    SleepTime = 0

    # Game loop
    # for CurrentCar in GameMode.Cars:
    #     if CurrentCar.IsDead:
    #         continue
    #     CurrentCar.Brain.Think(CurrentCar, GameMode)
    #     CurrentCar.React()

    # if ShouldDrawInfo:
    #     GameMode.DrawInfo()  # This slow down the game a lot
    time.sleep(SleepTime)

    GameMode.OnTurnEnd()

    # Update loop
    pygame.display.update()
    Clock.tick()
