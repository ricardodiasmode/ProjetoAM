import pygame
import background

# basic pygame setups
pygame.init()

currentBackground = background.Background()
currentBackground.drawBackground()

done = False
# event loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip()