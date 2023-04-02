import pygame
import background
import character
import inputHandler

# basic pygame setups
pygame.init()
clock = pygame.time.Clock()

current_background = background.Background()
current_background.drawBackground()

middle_of_screen = (current_background.display_width / 2, current_background.display_height / 2)
my_character = character.Character(middle_of_screen, current_background)

input_handler = inputHandler.InputHandler()

done = False
# event loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Handling keys
    input_handler.handle_input(current_background, my_character)

    # Update screen
    pygame.display.update()
    clock.tick(60)
