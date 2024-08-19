import json
import os

class LolAnalysis():
    def __init__(self) -> None:
        self.ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
        self.divisions = ["I", "II", "III", "IV"]
        self.high_elo = ["masterleagues", "grandmasterleagues", "challengerleagues"]

    def opt_num_games(self):
        k_wins = {}
        for i in range(13):
            k_wins[i] = [0, 0]
        print(k_wins)
        path = "LolData"
        for rank in self.high_elo:
            rank_path = "{0}/{1}".format(path, rank)
            for account in os.listdir(rank_path):
                account_path = "{0}/{1}".format(rank_path, account)
                last_game = 0
                k = 0
                for game in os.listdir(account_path):
                    game_path = "{0}/{1}".format(account_path, game)
                    print(game_path)
                    with open(game_path, "r") as file:
                        curr = json.load(file)
                        start = curr['info']['gameStartTimestamp']
                        end = curr['info']['gameEndTimestamp']
                        # if start - last_game > 1800:


