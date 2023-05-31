class GameMode:
    current_players_blue_team = 0
    current_players_red_team = 0
    characters = []
    last_alive = None

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
        pass

    def init_new_game(self):
        pass

    def reset_game(self):
        save_neural_network()
        random_mutations()
        init_new_game()



    #     FILE* f = fopen(String,"wb");
    #
    #     fwrite(&carros[indice].TamanhoDNA,  1,                              sizeof(int), f);
    #     fwrite(carros[indice].DNA,         carros[indice].TamanhoDNA,       sizeof(double), f);
    #
    #     fclose(f);
