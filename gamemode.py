import math
import random
import pygame
import background
import character


class GameMode:
    number_of_characters_each_team = 10
    generation = 0
    rangeRandom = 0

    current_background = None
    current_players_blue_team = 0
    current_players_red_team = 0
    characters = []
    best_alive_dna = None

    def init_new_game(self):
        print("Current generation: " + str(self.generation))
        self.current_players_blue_team = 0
        self.current_players_red_team = 0
        self.characters = []
        self.best_alive_dna = None

        self.current_background = background.Background()
        self.current_background.drawBackground()

        start_position_blue_team = (self.current_background.display_width / 4, 0)
        start_position_red_team = (start_position_blue_team[0] * 3, start_position_blue_team[1])

        for i in range(self.number_of_characters_each_team):
            self.characters.append(
                character.Character((start_position_blue_team[0], start_position_blue_team[1] + i * 64),
                                    self.current_background, self, True))
            self.current_players_blue_team += 1

        for i in range(self.number_of_characters_each_team):
            self.characters.append(
                character.Character((start_position_red_team[0], start_position_red_team[1] + i * 64),
                                    self.current_background, self, False))
            self.current_players_red_team += 1

    def check_if_game_over(self):
        if self.current_players_blue_team == 0 or self.current_players_red_team == 0:
            return True
        return False

    def random_mutations(self):
        TODO()

    def get_best_character_alive(self):
        for current_character in self.characters:
            # Check if any character has knife
            if current_character.has_knife:
                return current_character
            # Check if any character has log and rock
            if current_character.has_log and current_character.has_rock:
                return current_character
            # Check if any character has log
            if current_character.has_log:
                return current_character
            # Check if any character has rock
            if current_character.has_rock:
                return current_character
        if len(self.characters) > 0:
            return self.characters[0]
        return None

    def reset_game(self):
        if self.get_best_character_alive() is not None:
            self.best_alive_dna = self.get_best_character_alive().dna
        self.init_new_game()
        self.random_mutations()

    def update_closest_enemies(self):  # todo: optimize this to be better than O(n^2)
        for current_character in self.characters:
            closest_character = None
            for other_character in self.characters:
                if other_character != current_character:
                    if closest_character is None:
                        closest_character = other_character
                    else:
                        if current_character.distance_to(other_character) < current_character.distance_to(
                                closest_character):
                            closest_character = other_character
            current_character.closest_enemy = closest_character

    def get_all_characters_location(self, character_to_ignore=None):
        locations = []
        for current_character in self.characters:
            if current_character != character_to_ignore:
                locations.append(current_character.current_position)
        return locations

    def get_all_characters_location_with_team(self, character_to_ignore=None, blue_team=True):
        locations = []
        for current_character in self.characters:
            if current_character != character_to_ignore and current_character.current_team_is_blue == blue_team:
                locations.append(current_character.current_position)
        return locations


    def remove_player(self, character_to_remove):
        if character_to_remove.current_team_is_blue:
            self.current_players_blue_team -= 1
        else:
            self.current_players_red_team -= 1
        self.characters.remove(character_to_remove)
        self.update_closest_enemies()

    def write_text(self, message, x, y):
        font = pygame.font.SysFont("Arial", 18)
        text_color = (255, 255, 255)
        text = font.render(message, True, text_color)
        self.current_background.screen.blit(text, (x, y))

    def draw_simple_line(self, x, y, x2, y2, color):
        pygame.draw.line(self.current_background.screen, color, (x, y), (x2, y2))

    def draw_neuron(self, x, y, radius, color):
        pygame.draw.circle(self.current_background.screen, color, (x, y), radius)

    def draw_neural_network(self, x_location, y_location, width, height):
        entry_neuronX = []
        entry_neuronY = []
        hidden_neuronX = [[]]
        hidden_neuronY = [[]]
        out_neuronX = []
        out_neuronY = []
        mlp_input = []
        x_origin = x_location + 325
        y_origin = y_location + height
        neuron_size = 8

        best_character = self.get_best_character_alive()

        amount_hidden = best_character.brain.amount_of_hidden_layers
        amount_entry_neuron = best_character.brain.entry_layer.amount_neuron
        amount_neuron_hidden = best_character.brain.hidden_layer[0].amount_neuron
        amount_neuron_out = best_character.brain.out_layer.amount_neuron

        for i in range(best_character.brain.entry_layer.amount_neuron):
            mlp_input.append(best_character.brain.entry_layer.neurons[i].out_value)

        height_scale = 20 + height / (amount_neuron_hidden - 1)
        width_scale = (width - 475) / (amount_hidden + 1)

        temp = y_origin - (height_scale * (amount_neuron_hidden - 2)) / 2.0 + (
                height_scale * (amount_neuron_out - 1)) / 2.0

        self.write_text("Interagir", x_location + width - 130, temp - 0 * height_scale - 15)

        self.write_text("Andar para cima", x_location + width - 130, temp - 1 * height_scale - 15)

        self.write_text("Andar para baixo", x_location + width - 130, temp - 2 * height_scale - 15)

        self.write_text("Andar para direita", x_location + width - 130, temp - 3 * height_scale - 15)

        self.write_text("Andar para esquerda", x_location + width - 130, temp - 4 * height_scale - 15)

        # Drawing connections
        for i in range(amount_entry_neuron - 1):
            entry_neuronX.append(x_origin)
            entry_neuronY.append(y_origin - i * height_scale)

        for i in range(amount_hidden):
            if i == 0:
                amount_previous_layer = amount_entry_neuron
                x_previous = entry_neuronX
                y_previous = entry_neuronY
            else:
                amount_previous_layer = amount_neuron_hidden
                x_previous = hidden_neuronX[i - 1]
                y_previous = hidden_neuronY[i - 1]

            for j in range(amount_neuron_hidden - 1):
                hidden_neuronX[i].append(x_origin + (i + 1) * width_scale)
                hidden_neuronY[i].append(y_origin - j * height_scale)

                # Getting the greatest weight
                greatest_weight = 0
                greatest_weight_index = 0
                for k in range(amount_previous_layer - 1):
                    weight = best_character.brain.hidden_layer[i].neurons[j].weight[k]
                    if weight > greatest_weight:
                        greatest_weight = weight
                        greatest_weight_index = k
                self.draw_simple_line(x_previous[greatest_weight_index],
                                      y_previous[greatest_weight_index],
                                      hidden_neuronX[i][j],
                                      hidden_neuronY[i][j], (255, 0, 0))

                for k in range(amount_previous_layer - 1):
                    if k != greatest_weight_index:
                        self.draw_simple_line(x_previous[k],
                                              y_previous[k],
                                              hidden_neuronX[i][j],
                                              hidden_neuronY[i][j], (128, 128, 128))

        for i in range(amount_neuron_out):
            last_layer = best_character.brain.amount_of_hidden_layers - 1
            temp = y_origin - (height_scale * (amount_neuron_hidden - 2)) / 2.0 + (
                    height_scale * (amount_neuron_out - 1)) / 2.0

            out_neuronX.append(x_origin + (amount_hidden + 1) * width_scale)
            out_neuronY.append(temp - i * height_scale)

            # Getting the greatest weight
            greatest_weight = 0
            greatest_weight_index = 0
            for k in range(amount_neuron_hidden - 1):
                weight = best_character.brain.out_layer.neurons[i].weight[k]
                if weight > greatest_weight:
                    greatest_weight = weight
                    greatest_weight_index = k
            self.draw_simple_line(hidden_neuronX[last_layer][greatest_weight_index],
                                  hidden_neuronY[last_layer][greatest_weight_index],
                                  out_neuronX[i],
                                  out_neuronY[i], (255, 0, 0))

            for k in range(amount_neuron_hidden - 1):
                if k != greatest_weight_index:
                    self.draw_simple_line(hidden_neuronX[last_layer][k],
                                          hidden_neuronY[last_layer][k],
                                          out_neuronX[i],
                                          out_neuronY[i], (128, 128, 128))

        # Drawing neurons
        for i in range(amount_entry_neuron - 1):
            color = (0, 0, 0)
            self.draw_neuron(entry_neuronX[i],
                             entry_neuronY[i],
                             neuron_size * 1.3, color)

            if best_character.brain.entry_layer.neurons[i].out_value > 0:
                self.draw_neuron(entry_neuronX[i],
                                 entry_neuronY[i],
                                 neuron_size, (255, 0, 0))

        for i in range(amount_hidden):
            for j in range(amount_neuron_hidden - 1):
                color = (0, 0, 0)
                neuron_output = best_character.brain.hidden_layer[i].neurons[j].out_value
                if neuron_output > 0:
                    color = (255, 0, 0)

                self.draw_neuron(hidden_neuronX[i][j],
                                 hidden_neuronY[i][j],
                                 neuron_size * 1.3, (0, 0, 0))

                self.draw_neuron(hidden_neuronX[i][j],
                                 hidden_neuronY[i][j],
                                 neuron_size, color)

        best_neuron_index = 0
        for i in range(amount_neuron_out):
            if best_character.brain.out_layer.neurons[i].out_value > \
                    best_character.brain.out_layer.neurons[best_neuron_index].out_value:
                best_neuron_index = i

        for i in range(amount_neuron_out):
            color = (0, 0, 0)
            if i == best_neuron_index:
                color = (255, 0, 0)

            self.draw_neuron(
                out_neuronX[i],
                out_neuronY[i],
                neuron_size * 1.3, (0, 0, 0))

            self.draw_neuron(
                out_neuronX[i],
                out_neuronY[i],
                neuron_size, color)
