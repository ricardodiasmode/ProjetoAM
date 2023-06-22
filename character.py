import math
import random
import time

import utils
import pygame
import neuralNetwork


class Character:
    current_position = (0, 0)
    playerImg = pygame.image.load('BlueCharacter.png')
    has_log = False
    has_rock = False
    has_knife = False
    current_game_mode = None
    current_team_is_blue = False
    closest_enemy = None
    energy = 50
    dead = False

    brain = None
    dna = []

    def __init__(self, position, current_background, game_mode, blue_team):
        self.current_position = position
        self.current_game_mode = game_mode
        self.current_team_is_blue = blue_team
        self.update_image(current_background)

        # initializing neural network
        self.brain = neuralNetwork.neural_network_create()
        self.dna = []
        for i in range(neuralNetwork.neural_network_get_weight_amount(self.brain)):
            self.dna.append((random.randint(0, 20000) / 10.0) - 1000.0)

        if current_background.square_dict[self.current_position] == "LOG":
            self.remove_item_on_ground(current_background, "LOG")
        elif current_background.square_dict[self.current_position] == "ROCK":
            self.remove_item_on_ground(current_background, "ROCK")

    def move(self, position, current_background, game_mode):
        self.remove_energy(game_mode)
        location_to_go = (self.current_position[0] + position[0], self.current_position[1] + position[1])
        if utils.any_location_equal(location_to_go, game_mode.get_all_characters_location(self)):
            self.remove_energy(game_mode)
            return

        if location_to_go[0] < 0 or location_to_go[0] >= current_background.display_width or \
                location_to_go[1] < 0 or location_to_go[1] >= current_background.display_height:
            self.remove_energy(game_mode)
            return

        img_to_override = current_background.square_image_dict[self.current_position]
        current_background.screen.blit(img_to_override, self.current_position)
        self.current_position = location_to_go
        current_background.screen.blit(self.playerImg, self.current_position)

    def update_image(self, current_background):
        if self.has_log:
            if self.current_team_is_blue:
                self.playerImg = pygame.image.load('BlueCharacterWithLog.png')
            else:
                self.playerImg = pygame.image.load('RedCharacterWithLog.png')
        else:
            if self.current_team_is_blue:
                self.playerImg = pygame.image.load('BlueCharacter.png')
            else:
                self.playerImg = pygame.image.load('RedCharacter.png')
        current_background.screen.blit(self.playerImg, self.current_position)

    def remove_item_on_ground(self, current_background, item):
        if item == "LOG":
            current_background.screen.blit(self.playerImg, self.current_position)
            current_background.square_dict[self.current_position] = "GRASS"
            current_background.square_image_dict[self.current_position] = current_background.grass1Img
        else:
            current_background.screen.blit(current_background.grass3Img, self.current_position)
            current_background.screen.blit(self.playerImg, self.current_position)
            current_background.square_dict[self.current_position] = "GRASS"
            current_background.square_image_dict[self.current_position] = current_background.grass3Img

    def on_interact(self, current_background, game_mode):
        self.remove_energy(game_mode)
        if current_background.square_dict[self.current_position] == "LOG":
            if self.has_log or self.has_knife:
                self.remove_energy(game_mode)
                return
            print("GOT LOG!")
            self.has_log = True
            self.remove_item_on_ground(current_background, "LOG")
            self.update_image(current_background)

    def can_create_knife(self):
        return not self.has_knife and self.has_log \
            and self.has_rock

    def on_craft_knife_pressed(self, current_background, game_mode):
        self.remove_energy(game_mode)
        if self.can_create_knife():
            print("CRAFTED KNIFE!")
            time.sleep(10)
            self.has_log = False
            self.has_rock = False
            self.has_knife = True
            if self.current_team_is_blue:
                self.playerImg = pygame.image.load('BlueCharacterWithKnife.png')
            else:
                self.playerImg = pygame.image.load('RedCharacterWithKnife.png')
            current_background.screen.blit(self.playerImg, self.current_position)
        else:
            self.remove_energy(game_mode)

    def on_attack_pressed(self, game_mode):
        self.remove_energy(game_mode)

        if self.closest_enemy is None:
            self.remove_energy(game_mode)
            return

        if not (math.fabs(self.closest_enemy.current_position[0] - self.current_position[0]) < 90 and
                math.fabs(self.closest_enemy.current_position[1] - self.current_position[1]) < 90):
            self.remove_energy(game_mode)
            return

        if not self.has_knife:
            self.remove_energy(game_mode)
            return

        self.attack(game_mode)

    def attack(self, game_mode):
        self.closest_enemy.die(game_mode)
        self.closest_enemy = None
        self.energy = 25
        print("ATTACKED!")

    def walk_left(self, current_background, game_mode):
        self.move((-64, 0), current_background, game_mode)

    def walk_right(self, current_background, game_mode):
        self.move((64, 0), current_background, game_mode)

    def walk_up(self, current_background, game_mode):
        self.move((0, -64), current_background, game_mode)

    def walk_down(self, current_background, game_mode):
        self.move((0, 64), current_background, game_mode)

    def walk_to_closest_enemy(self, current_background, game_mode):
        if self.closest_enemy is None:
            return
        if self.closest_enemy.current_position[0] < self.current_position[0]:
            self.walk_left(current_background, game_mode)
        elif self.closest_enemy.current_position[0] > self.current_position[0]:
            self.walk_right(current_background, game_mode)
        elif self.closest_enemy.current_position[1] < self.current_position[1]:
            self.walk_up(current_background, game_mode)
        elif self.closest_enemy.current_position[1] > self.current_position[1]:
            self.walk_down(current_background, game_mode)

    def walk_to_closest_log(self, current_background, game_mode):
        closest_log_index = 0
        closest_log_dist = 0
        for current_log_location in current_background.logs_location:
            current_dist = self.distance_to_location(current_log_location)
            if current_dist < closest_log_dist or closest_log_dist == 0:
                closest_log_dist = current_dist
                closest_log_index = current_log_location
        if closest_log_index[0] < self.current_position[0]:
            self.walk_left(current_background, game_mode)
        elif closest_log_index[0] > self.current_position[0]:
            self.walk_right(current_background, game_mode)
        elif closest_log_index[1] < self.current_position[1]:
            self.walk_up(current_background, game_mode)
        elif closest_log_index[1] > self.current_position[1]:
            self.walk_down(current_background, game_mode)

    def die(self, game_mode):
        if self.dead:
            return
        img_to_override = game_mode.current_background.square_image_dict[self.current_position]
        game_mode.current_background.screen.blit(img_to_override, self.current_position)
        if self.current_team_is_blue:
            game_mode.current_players_blue_team -= 1
        else:
            game_mode.current_players_red_team -= 1
        self.dead = True

    def distance_to(self, character):
        return math.sqrt((self.current_position[0] - character.current_position[0]) ** 2 + (
                self.current_position[1] - character.current_position[1]) ** 2)

    def distance_to_location(self, location):
        return math.sqrt((self.current_position[0] - location[0]) ** 2 + (
                self.current_position[1] - location[1]) ** 2)

    def remove_energy(self, game_mode):
        self.energy -= 1
        if self.energy < 0:
            self.die(game_mode)
