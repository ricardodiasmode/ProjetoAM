import random
import background
import character


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
            file.write(str(self.last_alive.brain.dna[i]) + "\n")
        # close file
        file.close()

    def random_mutations(self):
        if self.generation == 0:
            self.rangeRandom = self.characters[0].dna[0]

        # Order characters by fitness using bubble sort. todo: optimize this to quick sort or merge sort?
        for i in range(len(self.characters)):
            for j in range(len(self.characters[i].dna)):
                if self.characters[j].fitness < self.characters[j + 1].fitness:
                    temp = self.characters[j]
                    self.characters[j] = self.characters[j + 1]
                    self.characters[j + 1] = temp

        # Cloning first 5 characters
        step = 5
        for i in range(step):
            for j in range(i + step, self.characters[i], step):
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
            self.characters.append(character.Character((start_position_blue_team[0], start_position_blue_team[1]+i*64),
                                                       self.current_background, self, True))
            self.current_players_blue_team += 1

        for i in range(self.number_of_characters_each_team):
            self.characters.append(character.Character((start_position_red_team[0], start_position_red_team[1]+i*64),
                                                       self.current_background, self, True))
            self.current_players_blue_team += 1

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

    def remove_player(self, character_to_remove):

        if character_to_remove.current_team_is_blue:
            self.current_players_blue_team -= 1
        else:
            self.current_players_red_team -= 1
        self.characters.remove(character_to_remove)
        self.update_closest_enemies()

        if len(self.characters) == 1:
            self.last_alive = self.characters[0]
