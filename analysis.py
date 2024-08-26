import json
import os
from collections import defaultdict

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


    def time_of_game(match):
        game_creation = match['info']['gameCreation']
        game_duration = match['info']['gameDuration']

        return game_creation + game_duration

# Tracking win ratio within sessions

    def did_win(puuid, match_data):
        win_index = match_data['metadata']['participants'].index(puuid)
        return match_data['info']['participants'][win_index]['win']

    def track_session(puuid, directory):
    
        sessions = []
        current_session = []
        previous_game_time = 0
        puuid = puuid

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                match = json.load(file)


            time = match['info']['gameCreation']

            if not current_session:

                if did_win(puuid, match):
                    current_session.append(1)
                else:
                    current_session.append(0)

            else:
            
                if time - previous_game_time <= 1800000:
                    if did_win(puuid, match):
                        current_session.append(1)
                    else:
                        current_session.append(0)

                else:
                    sessions.append(current_session)
                    if did_win(puuid, match):
                        current_session = [1]
                    else:
                        current_session = [0]
            
            previous_game_time = time_of_game(match)

        if current_session:
            sessions.append(current_session)

        return sessions

# Work with json files

    def avg_wr_for_session_length(sessions):

        session_win_rates = []
        for session in sessions:
            session_length = len(session)
            win_rate = sum(session) / session_length
            session_win_rates.append((session_length, win_rate))

        grouped_winrates = defaultdict(list)

        for session_length, win_rate in session_win_rates:
            grouped_winrates[session_length].append(win_rate)

        grouped_winrates = {k: [sum(v) / len(v), len(v)] for k, v in grouped_winrates.items()}

        return dict(sorted(grouped_winrates.items()))

    def avg_for_all_players(outputs):
    
        combined_dict = defaultdict(lambda: [0, 0])

        for d in outputs:
            for key, value in d.items():
                sum = value[0] * value[1]
                combined_dict[key][0] += sum
                combined_dict[key][1] += value[1]

        for k, v in combined_dict.items():
            total_sum = v[0]
            total_occurences = v[1]
            fianl_sum = total_sum / total_occurences
            combined_dict[k][0] = fianl_sum

        combined_dict = dict(combined_dict)

        return dict(sorted(combined_dict.items()))


    def get_to_work(ranked_games):
            poo = []
            for subdir in os.listdir(ranked_games):
                puuid = subdir
                subdir_path = os.path.join(ranked_games, subdir)

                try:
                    fart = track_session(puuid, subdir_path)
                    fart2 = avg_wr_for_session_length(fart)
                    poo.append(fart2)
                
                except Exception as e:
                    print("womp womp")

            fart3 = avg_for_all_players(poo)
            print(fart3)

def find_streak_wr(puuid, directory):

    current_win_streak = 0
    current_loss_streak = 0
    win_following_streak = defaultdict(list)
    loss_following_streak = defaultdict(list)

    for filename in os.listdir(directory):
        
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            match = json.load(file)

        result = did_win(puuid, match)
        
        #win game
        
        if result == True:

            if current_win_streak >= 3:
                win_following_streak[current_win_streak].append(1)
            if current_loss_streak >= 3:
                loss_following_streak[current_loss_streak].append(1)
            
            current_loss_streak = 0
            current_win_streak += 1

        #lose game
        
        else:

            if current_loss_streak >= 3:
                loss_following_streak[current_loss_streak].append(0)
            if current_win_streak >= 3:
                win_following_streak[current_win_streak].append(0)
                current_win_streak = 0

            current_win_streak = 0
            current_loss_streak += 1

    win_percentage_after_win_streak = {
        streak: [sum(results) / len(results), len(results)]
        for streak, results in win_following_streak.items()
            }

    win_percentage_after_loss_streak = {
        streak: [sum(results) / len(results), len(results)]
        for streak, results in loss_following_streak.items()
            }

    return [win_percentage_after_win_streak, win_percentage_after_loss_streak]

def avg_for_all(outputs):
    
    combined_dict_wins = defaultdict(lambda: [0, 0])
    combined_dict_losses = defaultdict(lambda: [0, 0])

    for d in outputs:
        for key, value in d[0].items():
            sum = value[0] * value[1]
            combined_dict_wins[key][0] += sum
            combined_dict_wins[key][1] += value[1]

        for key, value in d[1].items():
            sum = value[0] * value[1]
            combined_dict_losses[key][0] += sum
            combined_dict_losses[key][1] += value[1]

    for k, v in combined_dict_wins.items():
        total_sum = v[0]
        total_occurences = v[1]
        fianl_sum = total_sum / total_occurences
        combined_dict_wins[k][0] = fianl_sum

    combined_dict_wins = dict(combined_dict_wins)

    for k, v in combined_dict_losses.items():
        total_sum = v[0]
        total_occurences = v[1]
        fianl_sum = total_sum / total_occurences
        combined_dict_losses[k][0] = fianl_sum

    combined_dict_losses = dict(combined_dict_losses)

    return "Win percentage after X wins: " + str(dict(sorted(combined_dict_wins.items()))), "Win percentage after X losses: " + str(dict(sorted(combined_dict_losses.items())))

    
def go_time(ranked_games):
    yes = []
    for subdir in os.listdir(ranked_games):
        puuid = subdir
        subdir_path = os.path.join(ranked_games, subdir)

        try: 
            fart = find_streak_wr(puuid, subdir_path)
            yes.append(fart)

        except Exception as e:
            print("womp womp")

    fart3 = avg_for_all(yes)
    print(fart3)


go_time(challenger_games)

