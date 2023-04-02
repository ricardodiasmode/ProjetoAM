import pygame


class Character:
    current_position = (0, 0)
    playerImg = pygame.image.load('BlueCharacter.png')
    has_feather = False
    has_vine = False
    has_log = False
    has_rock = False

    def __init__(self, position, current_background):
        list_of_tuple = list(position)
        list_of_tuple[1] += 24 # image offset
        position = tuple(list_of_tuple)
        self.current_position = position
        current_background.screen.blit(self.playerImg, position)

    def add_position(self, position, current_background):
        img_to_override = current_background.square_image_dict[self.current_position]
        current_background.screen.blit(img_to_override, self.current_position)
        list_of_tuple = list(self.current_position)
        list_of_tuple[0] += position[0]
        list_of_tuple[1] += position[1]
        position = tuple(list_of_tuple)
        self.current_position = position
        current_background.screen.blit(self.playerImg, self.current_position)

    def on_interact(self, current_background):
        if current_background.square_dict[self.current_position] == "CHICKEN":
            if self.has_feather:
                return
            self.has_feather = True
            current_background.screen.blit(current_background.grass0Img, self.current_position)
            current_background.screen.blit(self.playerImg, self.current_position)
            current_background.square_dict[self.current_position] = "GRASS"
            current_background.square_image_dict[self.current_position] = current_background.grass0Img

        if current_background.square_dict[self.current_position] == "LOG":
            if self.has_log:
                return
            self.has_log = True
            current_background.screen.blit(current_background.grass1Img, self.current_position)
            current_background.screen.blit(self.playerImg, self.current_position)
            current_background.square_dict[self.current_position] = "GRASS"
            current_background.square_image_dict[self.current_position] = current_background.grass1Img

        if current_background.square_dict[self.current_position] == "TREE":
            if self.has_vine:
                return
            self.has_vine = True
            current_background.screen.blit(current_background.grass2Img, self.current_position)
            current_background.screen.blit(self.playerImg, self.current_position)
            current_background.square_dict[self.current_position] = "GRASS"
            current_background.square_image_dict[self.current_position] = current_background.grass2Img

        if current_background.square_dict[self.current_position] == "ROCK":
            if self.has_rock:
                return
            self.has_rock = True
            current_background.screen.blit(current_background.grass3Img, self.current_position)
            current_background.screen.blit(self.playerImg, self.current_position)
            current_background.square_dict[self.current_position] = "GRASS"
            current_background.square_image_dict[self.current_position] = current_background.grass3Img
