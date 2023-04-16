import pygame
import background
import character
import neuralNetwork
import gamemode
import math
import time


def basic_setups(current_clock, current_game_mode, current_background):
    # basic pygame setups
    pygame.init()
    current_clock = pygame.time.Clock()

    # basic game setups
    current_background.drawBackground()
    middle_of_screen = (current_background.display_width / 2, current_background.display_height / 2)
    number_of_characters_each_team = 1
    for i in range(number_of_characters_each_team * 2):
        current_game_mode.characters.append(character.Character(middle_of_screen, current_background, current_game_mode, i >= number_of_characters_each_team/2))


def get_closest_location(location_to_compare, locations_array):
    closest_location_index = 0
    closest_distance = 9999999
    for i in range(len(locations_array)):
        current_dist = math.sqrt((location_to_compare[0] - locations_array[i][0]) ** 2 + (
                    location_to_compare[1] - locations_array[i][1]) ** 2)
        if closest_distance > current_dist:
            closest_distance = current_dist
            closest_location_index = i
    return closest_location_index


def get_entry_params(current_character_ref, current_background_ref):
    entry_params_to_return = [current_character_ref.has_knife, current_character_ref.has_log, current_character_ref.has_rock,
                  current_character_ref.can_create_tent(), current_character_ref.can_create_knife(),
                  get_closest_location(current_character_ref.current_position, current_background_ref.rocks_location),
                  get_closest_location(current_character_ref.current_position, current_background_ref.logs_location),
                  get_closest_location(current_character_ref.current_position, current_background_ref.characters_location)]

    return entry_params_to_return


def react_given_out_param(current_character, out_params):
    if out_params[0]:
        current_character.move((0, -64))
    elif out_params[1]:
        current_character.move((0, 64))
    elif out_params[2]:
        current_character.move((-64, 0))
    elif out_params[3]:
        current_character.move((64, 0))
    elif out_params[4]:
        current_character.attack()
    elif out_params[5]:
        current_character.on_interact()
    elif out_params[6]:
        current_character.on_interact()
    elif out_params[7]:
        current_character.on_craft_tent_pressed()
    elif out_params[8]:
        current_character.on_craft_knife_pressed()


clock = None
game_mode = gamemode.GameMode()
current_background = background.Background()
basic_setups(clock, game_mode, current_background)
done = False
# event loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for current_character in game_mode.characters:
        entry_params = get_entry_params(current_character, current_background)
        neuralNetwork.neural_network_copy_to_entry_layer(current_character.brain, entry_params)
        neuralNetwork.neural_network_calculate_weights(current_character.brain)
        out_params = neuralNetwork.neural_network_copy_weights(current_character.brain)
        react_given_out_param(current_character, out_params)

    # Update screen
    pygame.display.update()
    clock.tick(60)

    # we need to see what is happenning
    time.sleep(0.1)
