import requests
import os
from dotenv import load_dotenv
import csv
import time

load_dotenv()
riot_api = os.environ["RIOT_API"]
ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
divisions = ["I", "II", "III", "IV"]
high_elo = ["masterleagues", "grandmasterleagues", "challengerleagues"]

for rank in ranks:
    for division in divisions:
        num_accounts = 0
        page = 1
        file_path = "data/{0}_{1}".format(rank, division)
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["leagueId", "queueType", 
                             "tier", "rank", "summonerId", 
                             "leaguePoints", "wins", "losses", 
                             "veteran", "inactive", "freshBlood", 
                             "hotStreak"])
            while num_accounts < 100:
                curr_rank = "https://na1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{0}/{1}?page={2}&api_key={3}".format(rank, division, str(page), riot_api)
                response = requests.get(curr_rank)
                while response.status_code == 429:
                    time.sleep(10)
                    response = requests.get(curr_rank)
                accounts = response.json()
                for i in range(len(accounts)):
                    curr_account = accounts[i]
                    if curr_account["wins"] + curr_account["losses"] > 200:
                        writer.writerow([curr_account["leagueId"], curr_account["queueType"], 
                            curr_account["tier"], curr_account["rank"], curr_account["summonerId"], 
                            curr_account["leaguePoints"], curr_account["wins"], curr_account["losses"], 
                            curr_account["veteran"], curr_account["inactive"], curr_account["freshBlood"], 
                            curr_account["hotStreak"]])
                        num_accounts += 1
                        if num_accounts >= 100:
                            break
                page += 1

for rank in high_elo:
    file_path = "data/{0}".format(rank)
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["summonerId", "leaguePoints",
                         "rank", "wins", "losses", 
                         "veteran", "inactive", 
                         "freshBlood", "hotStreak"])
        curr_rank = "https://na1.api.riotgames.com/lol/league/v4/{0}/by-queue/RANKED_SOLO_5x5?api_key={1}".format(rank, riot_api)
        response = requests.get(curr_rank)
        while response.status_code == 429:
            time.sleep(10)
            response = requests.get(curr_rank)
        accounts = response.json()["entries"]
        for i in range(len(accounts)):
            curr_account = accounts[i]
            writer.writerow([curr_account["summonerId"], curr_account["leaguePoints"], 
                                curr_account["rank"], curr_account["wins"], curr_account["losses"], 
                                curr_account["veteran"], curr_account["inactive"], 
                                curr_account["freshBlood"], curr_account["hotStreak"]])
