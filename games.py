import requests
import json
import os
from dotenv import load_dotenv
import time
import pandas as pd

load_dotenv()
riot_api = os.environ["RIOT_API"]
ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
divisions = ["I", "II", "III", "IV"]
high_elo = ["masterleagues", "grandmasterleagues", "challengerleagues"]

for rank in ranks:
    for division in divisions:
        path = "summoner_matches/{0}/{1}".format(rank, division)
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = "accounts/{0}_{1}.csv".format(rank, division)
        accounts = pd.read_csv(file_path)
        for index, row in accounts.iterrows():
            summoner_id = row["summonerId"]
            summoner_api = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/{0}?api_key={1}".format(summoner_id, riot_api)
            response = requests.get(summoner_api)
            while response.status_code == 429:
                print(response.status_code)
                time.sleep(10)
                response = requests.get(summoner_api)
            summoner = response.json()
            puuid = summoner["puuid"]
            matches_api = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?type=ranked&count=100&api_key={1}".format(puuid, riot_api)
            response = requests.get(matches_api)
            while response.status_code == 429:
                print(response.status_code)
                time.sleep(10)
                response = requests.get(matches_api)
            matches = response.json()
            summoner["rank"] = row["rank"]
            summoner["tier"] = row["tier"]
            summoner["wins"] = row["wins"]
            summoner["losses"] = row["losses"]
            summoner["matches"] = matches
            json_path = "summoner_matches/{0}/{1}/{2}.json".format(rank, division, summoner_id)
            json_file = json.dumps(summoner, indent=4)
            with open(json_path, "w") as file:
                file.write(json_file)

for rank in high_elo:
    path = "summoner_matches/{0}".format(rank)
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = "accounts/{0}.csv".format(rank)
    accounts = pd.read_csv(file_path)
    for index, row in accounts.iterrows():
        summoner_id = row["summonerId"]
        summoner_api = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/{0}?api_key={1}".format(summoner_id, riot_api)
        response = requests.get(summoner_api)
        while response.status_code == 429:
            print(response.status_code)
            time.sleep(10)
            response = requests.get(summoner_api)
        summoner = response.json()
        puuid = summoner["puuid"]
        matches_api = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?type=ranked&count=100&api_key={1}".format(puuid, riot_api)
        response = requests.get(matches_api)
        while response.status_code == 429:
            print(response.status_code)
            time.sleep(10)
            response = requests.get(matches_api)
        matches = response.json()
        summoner["rank"] = row["rank"]
        summoner["wins"] = row["wins"]
        summoner["losses"] = row["losses"]
        summoner["matches"] = matches
        json_path = "summoner_matches/{0}/{1}.json".format(rank, summoner_id)
        json_file = json.dumps(summoner, indent=4)
        with open(json_path, "w") as file:
            file.write(json_file)