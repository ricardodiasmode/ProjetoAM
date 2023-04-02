import pygame
import time


class InputHandler:

    def __init__(self):
        print("InputHandler created.")

    def handle_input(self, current_background, my_character):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            list_of_tuple = list(my_character.current_position)
            list_of_tuple[1] += -64
            position = tuple(list_of_tuple)
            if current_background.square_image_dict[position] == "RIVER":
                return
            my_character.add_position((0, -64), current_background)
            pygame.display.update()
            time.sleep(0.5)
        if pressed[pygame.K_s]:
            list_of_tuple = list(my_character.current_position)
            list_of_tuple[1] += 64
            position = tuple(list_of_tuple)
            if current_background.square_image_dict[position] == "RIVER":
                return
            my_character.add_position((0, 64), current_background)
            pygame.display.update()
            time.sleep(0.5)
        if pressed[pygame.K_a]:
            list_of_tuple = list(my_character.current_position)
            list_of_tuple[0] += -64
            position = tuple(list_of_tuple)
            if current_background.square_image_dict[position] == "RIVER":
                return
            my_character.add_position((-64, 0), current_background)
            pygame.display.update()
            time.sleep(0.5)
        if pressed[pygame.K_d]:
            list_of_tuple = list(my_character.current_position)
            list_of_tuple[0] += 64
            position = tuple(list_of_tuple)
            if current_background.square_image_dict[position] == "RIVER":
                return
            my_character.add_position((64, 0), current_background)
            pygame.display.update()
            time.sleep(0.5)
        if pressed[pygame.K_e]:
            my_character.on_interact(current_background)
