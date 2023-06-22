import pygame
import neuralNetwork
import gamemode
import time
import utils


def get_entry_params(current_character_ref, current_background_ref, game_mode_ref):
    closest_log_location = utils.get_closest_location(current_character_ref.current_position,
                                                      current_background_ref.logs_location)
    closest_log_distance = (current_character_ref.current_position[0] - \
                            current_background_ref.logs_location[closest_log_location][0],
                            current_character_ref.current_position[1] - \
                            current_background_ref.logs_location[closest_log_location][1])

    # get closest enemy location
    enemy_locations = game_mode_ref.get_all_characters_location_with_team(
        blue_team=not current_character_ref.current_team_is_blue)
    closest_enemy_distance = (999, 999)
    if len(enemy_locations) != 0:
        closest_enemy_location = utils.get_closest_location(current_character_ref.current_position,
                                                            enemy_locations)
        closest_enemy_distance = (current_character_ref.current_position[0] - \
                              enemy_locations[closest_enemy_location][0],
                              current_character_ref.current_position[1] - \
                              enemy_locations[closest_enemy_location][1])

    entry_params_to_return = [
        current_character_ref.has_knife,  # first param: has knife
        current_character_ref.has_log,  # second param: has log
        current_character_ref.can_create_knife(),  # fourth param: can create knife
        closest_log_distance[0],
        closest_log_distance[1],
        closest_enemy_distance[0],
        closest_enemy_distance[1]
    ]

    return entry_params_to_return


def react_given_out_param(current_background, current_character_ref, out_params_ref, in_game_mode):
    if out_params_ref[0]:
        current_character_ref.walk_to_closest_log(current_background, in_game_mode)
    elif out_params_ref[1]:
        current_character_ref.walk_to_closest_enemy(current_background, in_game_mode)
    elif out_params_ref[2]:
        current_character_ref.on_attack_pressed(in_game_mode)
    elif out_params_ref[3]:
        current_character_ref.on_interact(current_background, game_mode)
    elif out_params_ref[4]:
        current_character_ref.on_craft_knife_pressed(current_background, game_mode)


# basic pygame setups
pygame.init()

# basic game setups
clock = pygame.time.Clock()
game_mode = gamemode.GameMode()
game_mode.reset_game()

pygame.display.update()

done = False
current_turn = 0
# event loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for current_character in game_mode.characters:
        entry_params = get_entry_params(current_character, game_mode.current_background, game_mode)
        neuralNetwork.neural_network_copy_to_entry_layer(current_character.brain, entry_params)
        neuralNetwork.neural_network_calculate_weights(current_character.brain)
        out_params = neuralNetwork.neural_network_copy_weights(current_character.brain)
        react_given_out_param(game_mode.current_background, current_character, out_params, game_mode)
        game_mode.draw_neural_network(-230, 660, 600, 80)

    # Checking who dies this round
    game_mode.characters = [character for character in game_mode.characters if not character.dead]

    # Update screen
    pygame.display.update()
    clock.tick(240)

    # we need to see what is happening
    # time.sleep(0.001)

    current_turn += 1

    game_mode.update_closest_enemies()

    if game_mode.check_if_game_over():
        print("Game over in turn: " + str(current_turn))
        game_mode.reset_game()
        current_turn = 0
