import random

import pygame

import background
import character

AMOUNT_ENTRY_NEURON = character.AMOUNT_ENTRY_NEURON
AMOUNT_HIDDEN_NEURON = character.AMOUNT_HIDDEN_NEURON
AMOUNT_OUT_NEURON = character.AMOUNT_OUT_NEURON


class GameMode:
    number_of_characters_each_team = 1
    current_background = None
    current_players_blue_team = 0
    current_players_red_team = 0
    characters = []
    last_alive = None
    generation = 0
    rangeRandom = 0

    def check_if_game_over(self):
        if self.current_players_blue_team == 0 or self.current_players_red_team == 0:
            return True
        return False

    def save_neural_network(self):
        # creating file
        file = open("neural_network.txt", "w")
        # writing DNA
        for i in range(len(self.last_alive.dna)):
            file.write(str(self.last_alive.dna[i]) + "\n")
        # close file
        file.close()

    def random_mutations(self):
        if self.generation == 0:
            self.rangeRandom = self.characters[0].dna[0]

        # Order characters by fitness using bubble sort. todo: optimize this to quick sort or merge sort?
        for i in range(len(self.characters)):
            for j in range(len(self.characters) - 1):
                if self.characters[j].fitness < self.characters[j + 1].fitness:
                    temp = self.characters[j]
                    self.characters[j] = self.characters[j + 1]
                    self.characters[j + 1] = temp

        # Cloning first 5 characters
        step = 5
        for i in range(step):
            for j in range(i + step, len(self.characters), step):
                self.characters[j].dna = self.characters[i].dna

        # Mutating
        for j in range(step, len(self.characters)):
            mutations = random.randint(1, self.rangeRandom + 1)

            for k in range(mutations):
                tipo = random.randint(0, 2)
                indice = random.randint(0, len(self.characters[j].DNA) - 1)

                if tipo == 0:
                    self.characters[j].DNA[indice] = random.uniform(-1000.0, 1000.0)  # Valor Aleatório
                elif tipo == 1:
                    number = (random.randint(0, 10001) / 10000.0) + 0.5
                    self.characters[j].DNA[indice] = self.characters[j].DNA[indice] * number  # Multiplicação aleatória
                elif tipo == 2:
                    number = random.uniform(-1000.0, 1000.0) / 100.0
                    self.characters[j].DNA[indice] = self.characters[j].DNA[indice] + number  # Soma aleatória

        self.generation += 1

        self.rangeRandom = self.rangeRandom * 0.999
        if self.rangeRandom < 15:
            self.rangeRandom = 15

    def init_new_game(self):
        self.current_players_blue_team = 0
        self.current_players_red_team = 0
        self.characters = []
        self.last_alive = None
        self.generation = 0
        self.rangeRandom = 0

        self.current_background = background.Background()
        self.current_background.drawBackground()

        start_position_blue_team = (self.current_background.display_width / 4, -24)
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

    def reset_game(self):
        self.save_neural_network()
        self.random_mutations()
        self.init_new_game()

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

    def get_best_character_alive(self):
        for current_character in self.characters:
            # Check if any character has knife
            if current_character.has_knife:
                return current_character
            # Check if any character has log and rock
            if current_character.has_log and current_character.has_rock:
                return current_character
            # Check if any character has log or rock
            if current_character.has_log or current_character.has_rock:
                return current_character
        return self.characters[0]

    def remove_player(self, character_to_remove):

        if character_to_remove.current_team_is_blue:
            self.current_players_blue_team -= 1
        else:
            self.current_players_red_team -= 1
        self.characters.remove(character_to_remove)
        self.update_closest_enemies()

        if len(self.characters) == 1:
            self.last_alive = self.characters[0]

    def write_text(self, message, x, y):
        font = pygame.font.SysFont("Arial", 24)  # Exemplo de fonte e tamanho
        text_color = (255, 255, 255)  # Exemplo de cor (branco)
        text = font.render(message, True, text_color)
        self.current_background.screen.blit(text, (x, y))

    def draw_neural_network(self, X, Y, width, height):
        entry_neuronX = [0] * AMOUNT_ENTRY_NEURON
        entry_neuronY = [0] * AMOUNT_ENTRY_NEURON
        hidden_neuronX = [[0] * AMOUNT_HIDDEN_NEURON for _ in range(len(AMOUNT_HIDDEN_NEURON))]
        hidden_neuronY = [[0] * AMOUNT_HIDDEN_NEURON for _ in range(len(AMOUNT_HIDDEN_NEURON))]
        out_neuronX = [0] * AMOUNT_OUT_NEURON
        out_neuronY = [0] * AMOUNT_OUT_NEURON

        input = [0] * AMOUNT_ENTRY_NEURON
        x_origin = X + 325
        y_origin = Y + height
        neuron_size = 20

        best_character = self.get_best_character_alive()

        amount_hidden = best_character.brain.amount_of_hidden_layers
        amount_entry_neuron = best_character.brain.entry_layer.amount_neuron
        amount_neuron_hidden = best_character.brain.hidden_layer[0].amount_neuron
        amount_neuron_out = best_character.brain.out_layer.amount_neuron

        for i in range(AMOUNT_ENTRY_NEURON):
            input[i] = best_character.brain.entry_layer.neurons[i].out_value

        height_scale = height / (amount_neuron_hidden - 1)
        width_scale = (width - 475) / (amount_hidden + 1)

        temp = y_origin - (height_scale * (amount_neuron_hidden - 2)) / 2.0 + (
                height_scale * (amount_neuron_out - 1)) / 2.0

        self.write_text("Cima", X + width - 130, temp - 0 * height_scale - 90)

        self.write_text("Baixo", X + width - 130, temp - 1 * height_scale - 90)

        self.write_text("Esquerda", X + width - 130, temp - 2 * height_scale - 90)

        self.write_text("Direita", X + width - 130, temp - 3 * height_scale - 90)

        self.write_text("Atacar", X + width - 130, temp - 4 * height_scale - 90)

        self.write_text("Pegar", X + width - 130, temp - 5 * height_scale - 90)

        self.write_text("Craft Tenda", X + width - 130, temp - 6 * height_scale - 90)

        self.write_text("Craft Faca", X + width - 130, temp - 7 * height_scale - 90)

        # Drawing connections
        
        for i in range(amount_entry_neuron - 1):
            entry_neuronX[i] = x_origin
            entry_neuronY[i] = y_origin - i * height_scale

        for i in range(amount_hidden):
            if i == 0:
                amount_previous_layer = amount_entry_neuron
                previous_layer = best_character.brain.entry_layer
                x_previous = entry_neuronX
                y_previous = entry_neuronY
            else:
                amount_previous_layer = amount_neuron_hidden
                previous_layer = best_character.brain.hidden_layer[i - 1]
                x_previous = hidden_neuronX[i - 1]
                y_previous = hidden_neuronY[i - 1]

            for j in range(amount_neuron_hidden - 1):
                hidden_neuronX[i][j] = x_origin + (i + 1) * width_scale
                hidden_neuronY[i][j] = y_origin - j * height_scale - 85

                for k in range(amount_previous_layer - 1):
                    weight = best_character.brain.hidden_layer[i].Neuronios[j].Peso[k]
                    out_value = previous_layer.Neuronios[k].Saida
                    if weight * out_value > 0:
                        DesenharLinhaSimples(x_previous[k],
                                             y_previous[k],
                                             hidden_neuronX[i][j],
                                             hidden_neuronY[i][j], VERMELHO)

                    else:
                        DesenharLinhaSimples(x_previous[k],
                                             y_previous[k],
                                             hidden_neuronX[i][j],
                                             hidden_neuronY[i][j], CINZA)

        for i in range(amount_neuron_out):
            UltimaCamada = melhorCarro.Cerebro.QuantidadeEscondidas - 1
            temp = y_origin - (height_scale * (amount_neuron_hidden - 2)) / 2.0 + (
                    height_scale * (amount_neuron_out - 1)) / 2.0

            out_neuronX[i] = x_origin + (amount_hidden + 1) * width_scale
            out_neuronY[i] = temp - i * height_scale - 85

            for k in range(amount_neuron_hidden - 1):
                Peso = melhorCarro.Cerebro.CamadaSaida.Neuronios[i].Peso[k]
                Saida = best_character.brain.hidden_layer[UltimaCamada].Neuronios[k].Saida

                if Peso * Saida > 0:
                    DesenharLinhaSimples(hidden_neuronX[UltimaCamada][k],
                                         hidden_neuronY[UltimaCamada][k],
                                         out_neuronX[i],
                                         out_neuronY[i], VERMELHO)

                else:
                    DesenharLinhaSimples(hidden_neuronX[UltimaCamada][k],
                                         hidden_neuronY[UltimaCamada][k],
                                         out_neuronX[i],
                                         out_neuronY[i], CINZA)

        # Desenhar Neuronios

        for i in range(amount_entry_neuron - 1):
            if i == AMOUNT_ENTRY_NEURON - 1:
                if input[i] > 15:
                    Opacidade = 1
                else:
                    Opacidade = abs(input[i]) / 15.0
                cor = calcularCor(Opacidade, BRANCO)
            else:
                if input[i] > 200.0:
                    Opacidade = 0
                else:
                    Opacidade = abs(200.0 - input[i]) / 200.0
                cor = calcularCor(Opacidade, BRANCO)

            DefinirColoracao(SpriteNeuronAtivado, cor)
            DefinirOpacidade(SpriteLuzAmarelo, Opacidade * 255)

            DesenharSprite(spriteContornoNeuronio,
                           entry_neuronX[i],
                           entry_neuronY[i],
                           neuron_size * 1.1,
                           neuron_size * 1.1, 0, 0)

            DesenharSprite(SpriteNeuronAtivado,
                           entry_neuronX[i],
                           entry_neuronY[i],
                           neuron_size,
                           neuron_size, 0, 0)

            DefinirColoracao(SpriteNeuronAtivado, BRANCO)

        for i in range(amount_hidden):
            for j in range(amount_neuron_hidden - 1):
                Sprite = SpriteNeuronDesativado
                SaidaNeuronio = best_character.brain.hidden_layer[i].Neuronios[j].Saida
                if SaidaNeuronio > 0:
                    Sprite = SpriteNeuronAtivado

                DesenharSprite(spriteContornoNeuronio,
                               hidden_neuronX[i][j],
                               hidden_neuronY[i][j],
                               neuron_size * 1.1,
                               neuron_size * 1.1, 0, 0)

                DesenharSprite(Sprite,
                               hidden_neuronX[i][j],
                               hidden_neuronY[i][j],
                               neuron_size,
                               neuron_size, 0, 0)

        for i in range(amount_neuron_out):
            Sprite = SpriteNeuronDesativado
            SaidaNeuronio = melhorCarro.Cerebro.CamadaSaida.Neuronios[i].Saida
            if SaidaNeuronio > 0.5:
                Sprite = SpriteNeuronAtivado

            DesenharSprite(spriteContornoNeuronio,
                           out_neuronX[i],
                           out_neuronY[i],
                           neuron_size * 1.1,
                           neuron_size * 1.1, 0, 0)

            DesenharSprite(Sprite,
                           out_neuronX[i],
                           out_neuronY[i],
                           neuron_size,
                           neuron_size, 0, 0)
