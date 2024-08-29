import os
from pathlib import Path
import json
import requests
from collections import defaultdict

# Optimal number of games per session
# 
# Must do the following:
# - Know how many games are played within the session definition (a new ranked solo queue game within a 20 minute period)
# - Must track win / loss ratio for each session

# General functions for completion

challenger_games = Path("E:/GOTIME/Lol-data/LolData/challengerleagues")

gm_games = Path("E:/GOTIME/Lol-data/LolData/grandmasterleagues")

master_games = Path("E:/GOTIME/Lol-data/LolData/masterleagues")

# Tracking time of games - and session lengths

def time_of_game(match):
    game_creation = match['info']['gameCreation']
    game_duration = match['info']['gameDuration']
    game_duration = game_duration * 1000

    return game_creation + game_duration

# Tracking win ratio within sessions

def did_win(puuid, match_data):
    win_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][win_index]['win']

def track_session(puuid, directory):
    
    sessions = []
    current_session = []
    previous_game_time = 0

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
        list_outputs = []
        for subdir in os.listdir(ranked_games):
            puuid = subdir
            subdir_path = os.path.join(ranked_games, subdir)

            try:
                tracked_sessions = track_session(puuid, subdir_path)
                avg_session_wr = avg_wr_for_session_length(tracked_sessions)
                list_outputs.append(avg_session_wr)
                
            except Exception as e:
                None

        final_avg = avg_for_all_players(list_outputs)
        return final_avg

yes = []
chall = get_to_work(challenger_games)
gm = get_to_work(gm_games)
master = get_to_work(master_games)
yes.append(chall)
yes.append(gm)
yes.append(master)
print(avg_for_all_players(yes))





    
  
    
    
    
    
    



