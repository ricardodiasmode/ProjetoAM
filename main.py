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

while GameMode.GameIsRunning:
    # Event loop
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            GameMode.GameIsRunning = False

    # Game loop
    for CurrentCharacter in GameMode.Characters:
        if CurrentCharacter.IsDead:
            continue
        CurrentCharacter.Brain.Think(CurrentCharacter, GameMode.CurrentBackground)
        CurrentCharacter.React()
        GameMode.DrawInfo()  # This slow down the game a lot

    GameMode.OnTurnEnd()

    # Update loop
    pygame.display.update()
    Clock.tick()
