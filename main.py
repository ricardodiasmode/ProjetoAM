import pygame
import neuralNetwork
import gamemode
import math
import time


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
    entry_params_to_return = [current_character_ref.has_knife, current_character_ref.has_log,
                              current_character_ref.has_rock,
                              current_character_ref.can_create_tent(), current_character_ref.can_create_knife(),
                              get_closest_location(current_character_ref.current_position,
                                                   current_background_ref.rocks_location),
                              get_closest_location(current_character_ref.current_position,
                                                   current_background_ref.logs_location),
                              get_closest_location(current_character_ref.current_position,
                                                   current_background_ref.characters_location)]

    return entry_params_to_return


def react_given_out_param(current_background, current_character_ref, out_params_ref):
    if out_params_ref[0]:
        current_character_ref.move((0, -64), current_background)
    elif out_params_ref[1]:
        current_character_ref.move((0, 64), current_background)
    elif out_params_ref[2]:
        current_character_ref.move((-64, 0), current_background)
    elif out_params_ref[3]:
        current_character_ref.move((64, 0), current_background)
    elif out_params_ref[4]:
        if current_character_ref.has_knife:
            current_character_ref.attack()
    elif out_params_ref[5]:
        current_character_ref.on_interact(current_background)
    elif out_params_ref[6]:
        current_character_ref.on_interact(current_background)
    elif out_params_ref[7]:
        current_character_ref.on_craft_tent_pressed()
    elif out_params_ref[8]:
        current_character_ref.on_craft_knife_pressed()


# basic pygame setups
pygame.init()

# basic game setups
clock = pygame.time.Clock()
game_mode = gamemode.GameMode()
game_mode.init_new_game()

done = False
current_turn = 0
# event loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for current_character in game_mode.characters:
        entry_params = get_entry_params(current_character, game_mode.current_background)
        neuralNetwork.neural_network_copy_to_entry_layer(current_character.brain, entry_params)
        neuralNetwork.neural_network_calculate_weights(current_character.brain)
        out_params = neuralNetwork.neural_network_copy_weights(current_character.brain)
        react_given_out_param(game_mode.current_background, current_character, out_params)

    # Update screen
    pygame.display.update()
    clock.tick(60)

    # we need to see what is happening
    time.sleep(0.1)

    # die after 10 turns if character has no knife
    if current_turn == 10:
        for current_character in game_mode.characters:
            if not current_character.has_knife:
                current_character.die(game_mode)

    # die after 20 turns if character has knife and didn't kill anyone
    if current_turn == 20:
        for current_character in game_mode.characters:
            if current_character.has_knife and not current_character.has_killed:
                current_character.die(game_mode)

    current_turn += 1

    game_mode.update_closest_enemies()

    if game_mode.check_if_game_over():
        game_mode.reset_game()
