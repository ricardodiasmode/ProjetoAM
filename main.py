import pygame
import neuralNetwork
import gamemode
import time
import utils


def get_entry_params(current_character_ref, current_background_ref):
    has_rock_below = utils.any_location_equal(current_character_ref.current_position, current_background_ref.rocks_location)
    has_log_below = utils.any_location_equal(current_character_ref.current_position, current_background_ref.logs_location)
    closest_enemy_location = utils.get_closest_location(current_character_ref.current_position,
                                                  game_mode.get_all_characters_location(current_character_ref))
    entry_params_to_return = [
        current_character_ref.has_knife,  # first param: has knife
        current_character_ref.has_log,  # second param: has log
        current_character_ref.has_rock,  # third param: has rock
        current_character_ref.can_create_tent(),  # fourth param: can create tent
        current_character_ref.can_create_knife(),  # fifth param: can create knife
        has_rock_below,  # sixth param: has rock below
        has_log_below,  # seventh param: has log below
        closest_enemy_location,  # eighth param: closest enemy
    ]

    return entry_params_to_return


def react_given_out_param(current_background, current_character_ref, out_params_ref, game_mode):
    if out_params_ref[0]:
        current_character_ref.move((0, -64), current_background, game_mode)
    elif out_params_ref[1]:
        current_character_ref.move((0, 64), current_background, game_mode)
    elif out_params_ref[2]:
        current_character_ref.move((-64, 0), current_background, game_mode)
    elif out_params_ref[3]:
        current_character_ref.move((64, 0), current_background, game_mode)
    elif out_params_ref[4]:
        if current_character_ref.has_knife:
            current_character_ref.attack()
    elif out_params_ref[5]:
        current_character_ref.on_interact(current_background)
    elif out_params_ref[6]:
        current_character_ref.on_craft_tent_pressed(current_background)
    elif out_params_ref[7]:
        current_character_ref.on_craft_knife_pressed(current_background)


# basic pygame setups
pygame.init()

# basic game setups
clock = pygame.time.Clock()
game_mode = gamemode.GameMode()
game_mode.reset_game()

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
        react_given_out_param(game_mode.current_background, current_character, out_params, game_mode)
        game_mode.draw_neural_network(-230, 660, 600, 80)

    # Update screen
    pygame.display.update()
    clock.tick(60)

    # we need to see what is happening
    time.sleep(0.001)

    # die after 10 turns if character has no log or stone
    if current_turn == 10:
        players_to_remove = []
        for current_character in game_mode.characters:
            if not current_character.has_log and not current_character.has_rock:
                current_character.die(game_mode)
                players_to_remove.append(current_character)
        print(f'removing {len(players_to_remove)}')
        for current_player in players_to_remove:
            game_mode.remove_player(current_player)
        if len(game_mode.characters) > 0:
            time.sleep(10)

    # die after 20 turns if character has no knife
    if current_turn == 20:
        players_to_remove = []
        for current_character in game_mode.characters:
            if not current_character.has_knife:
                current_character.die(game_mode)
                players_to_remove.append(current_character)
        for current_player in players_to_remove:
            game_mode.remove_player(current_player)

    # die after 30 turns if character has knife and didn't kill anyone
    if current_turn == 30:
        players_to_remove = []
        for current_character in game_mode.characters:
            if current_character.has_knife and not current_character.has_killed:
                current_character.die(game_mode)
                players_to_remove.append(current_character)
        for current_player in players_to_remove:
            game_mode.remove_player(current_player)

    current_turn += 1

    game_mode.update_closest_enemies()

    if game_mode.check_if_game_over():
        # print("Game over in turn: " + str(current_turn))
        game_mode.reset_game()
        current_turn = 0

    # print("Turn: " + str(current_turn) + " passed.")
