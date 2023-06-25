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
FrameRate = 0

while GameMode.GameIsRunning:
    # Event loop
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            GameMode.GameIsRunning = False
        if Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_s:
                ShouldDrawInfo = not ShouldDrawInfo
            elif Event.key == pygame.K_UP:
                FrameRate += 30
            elif Event.key == pygame.K_DOWN:
                FrameRate -= 30
                if FrameRate < 30:
                    FrameRate = 30

    # Game loop
    for CurrentCharacter in GameMode.Characters:
        if CurrentCharacter.IsDead:
            continue
        CurrentCharacter.Brain.Think(CurrentCharacter, GameMode)
        CurrentCharacter.React()
    if ShouldDrawInfo:
        GameMode.DrawInfo()  # This slow down the game a lot

    GameMode.OnTurnEnd()

    # Update loop
    pygame.display.update()
    Clock.tick(FrameRate)
