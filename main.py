import time

import pygame
import gamemode
import neuralNetwork

# Basic game setups
pygame.init()
Clock = pygame.time.Clock()
GameMode = gamemode.GameMode()
GameMode.ResetGame()
pygame.display.update()
ShouldDrawInfo = False
SleepTime = 0

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
    for CurrentCharacter in GameMode.Characters:
        if CurrentCharacter.IsDead:
            continue
        CurrentCharacter.Brain.Think(CurrentCharacter, GameMode)
        CurrentCharacter.React()
        time.sleep(SleepTime)
    if ShouldDrawInfo:
        GameMode.DrawInfo()  # This slow down the game a lot
    time.sleep(SleepTime*10)

    GameMode.OnTurnEnd()

    # Update loop
    pygame.display.update()
    Clock.tick()
