import json
import os

class LolAnalysis():
    def __init__(self) -> None:
        self.ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
        self.divisions = ["I", "II", "III", "IV"]
        self.high_elo = ["masterleagues", "grandmasterleagues", "challengerleagues"]

    def opt_num_games(self):
        """
        Function to determine the winrate of a game given k # of games 
        played before.
        """
        path = "LolData"
        total = {}
        for rank in self.high_elo:

            rank_path = "{0}/{1}".format(path, rank)
            k_wins = {}
            for i in range(13):
                k_wins[i] = [0, 0]

            for account in os.listdir(rank_path):

                account_path = "{0}/{1}".format(rank_path, account)
                last_game = 0
                k = 0

                for game in os.listdir(account_path):
                    game_path = "{0}/{1}".format(account_path, game)

                    with open(game_path, "r") as file:
                        curr = json.load(file)
                        if "status" not in curr.keys() and curr['info']['endOfGameResult'] == 'GameComplete':
                            result = self.game_result(curr, account)
                            if result:
                                result = 0
                            else:
                                result = 1
                            start = curr['info']['gameStartTimestamp']
                            end = curr['info']['gameEndTimestamp']
                            if start - last_game < 1800000:
                                if k >= 12:
                                    k_wins[12][result] += 1
                                else:
                                    k_wins[k][result] += 1
                                    k += 1
                            else:
                                k = 0
                                k_wins[k][result] += 1 
                            last_game = end

            total[rank] = k_wins
            print(rank_path, k_wins)

        for rank in self.ranks:
            for division in self.divisions: 

                k_wins = {}
                for i in range(13):
                    k_wins[i] = [0, 0]
                rank_path = "{0}/{1}/{2}".format(path, rank, division)

                for account in os.listdir(rank_path):

                    account_path = "{0}/{1}".format(rank_path, account)
                    last_game = 0
                    k = 0

                    for game in os.listdir(account_path):
                        game_path = "{0}/{1}".format(account_path, game)

                        with open(game_path, "r") as file:
                            curr = json.load(file)
                            if "status" not in curr.keys() and curr['info']['endOfGameResult'] == 'GameComplete':
                                result = self.game_result(curr, account)
                                if result:
                                    result = 0
                                else:
                                    result = 1
                                start = curr['info']['gameStartTimestamp']
                                end = curr['info']['gameEndTimestamp']
                                if start - last_game < 1800000:
                                    if k >= 12:
                                        k_wins[12][result] += 1
                                    else:
                                        k_wins[k][result] += 1
                                        k += 1
                                else:
                                    k = 0
                                    k_wins[k][result] += 1 
                                last_game = end

                total["{0}/{1}".format(rank, division)] = k_wins
                print(rank_path, k_wins)

        json_file = json.dumps(total, indent=4)
        with open("session_winrates.json", "w") as file:
            file.write(json_file)

    def game_result(self, game, puuid):
        """
        Function to determine if a player won the game.
        """
        index = game['metadata']['participants'].index(puuid)
        result = game['info']['participants'][index]['win']
        return result
    
    def breaks(self):
        """
        Function to determine winrate of a game after taking a break.
        """
        path = "LolData"
        total = {}
        for rank in self.high_elo:

            rank_path = "{0}/{1}".format(path, rank)
            breaks = {}
            breaks['wins'] = 0
            breaks['losses'] = 0

            for account in os.listdir(rank_path):

                account_path = "{0}/{1}".format(rank_path, account)
                last_game = 0
                last_game_result = ''

                for game in os.listdir(account_path):
                    game_path = "{0}/{1}".format(account_path, game)

                    with open(game_path, "r") as file:
                        curr = json.load(file)
                        if "status" not in curr.keys() and curr['info']['endOfGameResult'] == 'GameComplete':
                            result = self.game_result(curr, account)
                            if result:
                                result = 'wins'
                            else:
                                result = 'losses'
                            start = curr['info']['gameStartTimestamp']
                            end = curr['info']['gameEndTimestamp']
                            if start - last_game > 1800000 and start - last_game < 28800000 and last_game_result == "losses":
                                breaks[result] += 1
                            last_game = end
                            last_game_result = result
                            
            total[rank] = breaks
            print(rank_path, breaks)

        for rank in self.ranks:
            for division in self.divisions: 

                rank_path = "{0}/{1}/{2}".format(path, rank, division)
                breaks = {}
                breaks['wins'] = 0
                breaks['losses'] = 0

                for account in os.listdir(rank_path):

                    account_path = "{0}/{1}".format(rank_path, account)
                    last_game = 0
                    last_game_result = ""

                    for game in os.listdir(account_path):
                        game_path = "{0}/{1}".format(account_path, game)

                        with open(game_path, "r") as file:
                            curr = json.load(file)
                            if "status" not in curr.keys() and curr['info']['endOfGameResult'] == 'GameComplete':
                                result = self.game_result(curr, account)
                                if result:
                                    result = 'wins'
                                else:
                                    result = 'losses'
                                start = curr['info']['gameStartTimestamp']
                                end = curr['info']['gameEndTimestamp']
                                if start - last_game > 1800000 and start - last_game < 28800000 and last_game_result == "losses":
                                    breaks[result] += 1
                                last_game = end
                                last_game_result = result


                total["{0}/{1}".format(rank, division)] = breaks
                print(rank_path, breaks)

        json_file = json.dumps(total, indent=4)
        with open("breaks.json", "w") as file:
            file.write(json_file)
