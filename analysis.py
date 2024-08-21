import json
import os

class LolAnalysis():
    def __init__(self) -> None:
        self.ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
        self.divisions = ["I", "II", "III", "IV"]
        self.high_elo = ["masterleagues", "grandmasterleagues", "challengerleagues"]

    def opt_num_games(self):
        bad = 0
        k_wins = {}
        for i in range(13):
            k_wins[i] = [0, 0]
        path = "LolData"
        for rank in self.high_elo:
            rank_path = "{0}/{1}".format(path, rank)
            for account in os.listdir(rank_path):
                account_path = "{0}/{1}".format(rank_path, account)
                last_game = 0
                k = 0
                for game in os.listdir(account_path):
                    game_path = "{0}/{1}".format(account_path, game)
                    with open(game_path, "r") as file:
                        curr = json.load(file)
                        if "status" not in curr.keys():
                            start = curr['info']['gameStartTimestamp']
                            end = curr['info']['gameEndTimestamp']
                            if start - last_game < 1800000:
                                if k >= 12:
                                    k_wins[12][0] += 1
                                else:
                                    k_wins[k][0] += 1
                                    k += 1
                            else:
                                k = 0
                                k_wins[k][0] += 1 
                            last_game = end
                        else:
                            bad += 1
        print(k_wins)
        total = 0
        for i in range(13):
            total += k_wins[i][0]
        print(total, bad, total + bad)

        bad = 0
        k_wins = {}
        for i in range(13):
            k_wins[i] = [0, 0]
        path = "LolData"
        for rank in self.ranks:
            for division in self.divisions: 
                rank_path = "{0}/{1}/{2}".format(path, rank, division)
                for account in os.listdir(rank_path):
                    account_path = "{0}/{1}".format(rank_path, account)
                    last_game = 0
                    k = 0
                    for game in os.listdir(account_path):
                        game_path = "{0}/{1}".format(account_path, game)
                        with open(game_path, "r") as file:
                            curr = json.load(file)
                            if "status" not in curr.keys():
                                start = curr['info']['gameStartTimestamp']
                                end = curr['info']['gameEndTimestamp']
                                if start - last_game < 1800000:
                                    if k >= 12:
                                        k_wins[12][0] += 1
                                    else:
                                        k_wins[k][0] += 1
                                        k += 1
                                else:
                                    k = 0
                                    k_wins[k][0] += 1 
                                last_game = end
                            else:
                                bad += 1
        print(k_wins)
        total = 0
        for i in range(13):
            total += k_wins[i][0]
        print(total, bad, total + bad)


