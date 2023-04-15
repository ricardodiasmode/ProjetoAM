import pygame


class Character:
    current_position = (0, 0)
    playerImg = pygame.image.load('BlueCharacter.png')
    has_log = False
    has_rock = False
    has_knife = False
    current_game_mode = None
    current_team_is_blue = False

    def __init__(self, position, current_background, game_mode, blue_team):
        list_of_tuple = list(position)
        list_of_tuple[1] += 24 # image offset
        position = tuple(list_of_tuple)
        self.current_position = position
        current_background.screen.blit(self.playerImg, position)
        self.current_game_mode = game_mode
        self.current_team_is_blue = blue_team

    def ia_loop(self, all_rocks_locations, all_logs_location, all_enemy_characters_locations):


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

        if current_background.square_dict[self.current_position] == "LOG":
            if self.has_log:
                return
            self.has_log = True
            current_background.screen.blit(current_background.grass1Img, self.current_position)
            current_background.screen.blit(self.playerImg, self.current_position)
            current_background.square_dict[self.current_position] = "GRASS"
            current_background.square_image_dict[self.current_position] = current_background.grass1Img

        if current_background.square_dict[self.current_position] == "ROCK":
            if self.has_rock:
                return
            self.has_rock = True
            current_background.screen.blit(current_background.grass3Img, self.current_position)
            current_background.screen.blit(self.playerImg, self.current_position)
            current_background.square_dict[self.current_position] = "GRASS"
            current_background.square_image_dict[self.current_position] = current_background.grass3Img

    def on_craft_tent_pressed(self, current_background):
        self.try_create_tent(current_background)

    def can_create_tent(self):
        if not (self.has_log and self.has_rock):
            return False
        if self.current_team_is_blue:
            if self.current_game_mode.current_players_blue_team < 10:
                return True
        else:
            if self.current_game_mode.current_players_red_team < 10:
                return True
        return False

    def try_create_tent(self, current_background):
        if not self.can_create_tent():
            return
        self.create_tent(current_background)
        if self.current_team_is_blue:
            self.current_game_mode.current_players_blue_team += 1
        else:
            self.current_game_mode.current_players_red_team += 1

    def create_tent(self, current_background):
        self.has_rock = False
        self.has_log = False
        current_background.square_dict[self.current_position] = "TENT"
        current_background.square_image_dict[self.current_position] = current_background.tentImg
        current_background.screen.blit(current_background.tentImg, self.current_position)
        current_background.screen.blit(self.playerImg, self.current_position)
        # TODO: Create a AI character

    def can_create_knife(self):
        return not self.has_bow and not self.has_knife and self.has_log \
                and self.has_rock;

    def on_craft_knife_pressed(self, current_background):
        if self.can_create_knife():
            self.has_log = False
            self.has_rock = False
            self.has_vine = False
            self.has_feather = False
            self.has_knife = True
            if self.current_team_is_blue:
                self.playerImg = pygame.image.load('BlueCharacterWithKnife.png')
            else:
                self.playerImg = pygame.image.load('RedCharacterWithKnife.png')
            current_background.screen.blit(self.playerImg, self.current_position)
