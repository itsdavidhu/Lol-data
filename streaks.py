import os
from pathlib import Path
import json
import requests
from collections import defaultdict
from sessions import challenger_games, gm_games, master_games, did_win


#Streaks will track the winrates after a 3,4,5 game win/loss streak

plz = Path("E:/GOTIME/Lol-data/LolData/challengerleagues/0gNRCWOvpU6SPcPHR6wPfrxibIzCagHTKrwM57E9o5pI1WoLxemdmh8Poft2UkUGY9uqfmu6-wpqUw")

puuid = "0gNRCWOvpU6SPcPHR6wPfrxibIzCagHTKrwM57E9o5pI1WoLxemdmh8Poft2UkUGY9uqfmu6-wpqUw"

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

    return dict(sorted(combined_dict_wins.items())), dict(sorted(combined_dict_losses.items()))

def avg_for_all2(outputs):
    
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
    list_outputs = []
    for subdir in os.listdir(ranked_games):
        puuid = subdir
        subdir_path = os.path.join(ranked_games, subdir)

        try: 
            streak_wr = find_streak_wr(puuid, subdir_path)
            list_outputs.append(streak_wr)

        except Exception as e:
            None

    avg_for_all_ranks = avg_for_all(list_outputs)
    return avg_for_all_ranks

yes = []
chall = go_time(challenger_games)
gm = go_time(gm_games)
master = go_time(master_games)
yes.append(chall)
yes.append(gm)
yes.append(master)
print(avg_for_all2(yes))
