import requests
import os
from dotenv import load_dotenv
import csv
import time
import json
import pandas as pd

class LolData:
    def __init__(self) -> None:
        load_dotenv()
        self._riot_api = os.environ["RIOT_API"]
        self.ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
        self.divisions = ["I", "II", "III", "IV"]
        self.high_elo = ["masterleagues", "grandmasterleagues", "challengerleagues"]
        self.winrates = {}

    def load_general_accounts(self):
        """
        Function to load 100 accounts DIAMOND to IRON with more than 200 games played.
        """        
        for rank in self.ranks:
            for division in self.divisions:

                path = "accounts"
                if not os.path.exists(path):
                    os.makedirs(path)
                print("Generating accounts for {0} {1}".format(rank, division))
                file_path = "accounts/{0}_{1}.csv".format(rank, division)

                all_accounts = set()
                num_accounts = 0
                page = 1

                # Write account data to csv
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["leagueId", "queueType", 
                                    "tier", "rank", "summonerId", 
                                    "leaguePoints", "wins", "losses", 
                                    "veteran", "inactive", "freshBlood", 
                                    "hotStreak"])
                    
                    # Get 100 accounts
                    while num_accounts < 100:
                        curr_rank = "https://na1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{0}/{1}?page={2}&api_key={3}".format(rank, division, str(page), self._riot_api)
                        response = requests.get(curr_rank)
                        while response.status_code == 429:
                            time.sleep(10)
                            response = requests.get(curr_rank)
                        accounts = response.json()

                        for i in range(len(accounts)):
                            curr_account = accounts[i]
                            if curr_account["summonerId"] in all_accounts:
                                continue
                            if curr_account["wins"] + curr_account["losses"] > 200:
                                writer.writerow([curr_account["leagueId"], curr_account["queueType"], 
                                    curr_account["tier"], curr_account["rank"], curr_account["summonerId"], 
                                    curr_account["leaguePoints"], curr_account["wins"], curr_account["losses"], 
                                    curr_account["veteran"], curr_account["inactive"], curr_account["freshBlood"], 
                                    curr_account["hotStreak"]])
                                num_accounts += 1
                                all_accounts.add(curr_account["summonerId"])
                                if num_accounts >= 100:
                                    break
                        page += 1
    
    def load_high_elo_accounts(self):
        """
        Function to load all accounts in high elo (challenger, grandmaster, master).
        """       
        for rank in self.high_elo:

            path = "accounts"
            if not os.path.exists(path):
                os.makedirs(path)
            print("Generating accounts for {0}".format(rank))
            file_path = "accounts/{0}.csv".format(rank)

            # Write account data to csv
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["summonerId", "leaguePoints",
                                "rank", "wins", "losses", 
                                "veteran", "inactive", 
                                "freshBlood", "hotStreak"])
                curr_rank = "https://na1.api.riotgames.com/lol/league/v4/{0}/by-queue/RANKED_SOLO_5x5?api_key={1}".format(rank, self._riot_api)
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
                    
    def load_general_matches(self):
        """
        Function to load the match ids of the last 100 games for each account 
        generated between DIAMOND AND IRON.
        """
        for rank in self.ranks:
            for division in self.divisions:

                path = "summoner_matches/{0}/{1}".format(rank, division)
                if not os.path.exists(path):
                    os.makedirs(path)
                print("Generating matches for {0} {1}".format(rank, division))
                file_path = "accounts/{0}_{1}.csv".format(rank, division)

                # Read account data
                accounts = pd.read_csv(file_path)
                for index, row in accounts.iterrows():

                    summoner_id = row["summonerId"]
                    summoner_api = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/{0}?api_key={1}".format(summoner_id, self._riot_api)
                    response = requests.get(summoner_api)
                    while response.status_code == 429:
                        time.sleep(10)
                        response = requests.get(summoner_api)
                    summoner = response.json()

                    puuid = summoner["puuid"]
                    matches_api = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?type=ranked&count=100&api_key={1}".format(puuid, self._riot_api)
                    response = requests.get(matches_api)
                    while response.status_code == 429:
                        time.sleep(10)
                        response = requests.get(matches_api)
                    matches = response.json()

                    summoner["rank"] = row["rank"]
                    summoner["tier"] = row["tier"]
                    summoner["wins"] = row["wins"]
                    summoner["losses"] = row["losses"]
                    summoner["matches"] = matches
                    
                    # Write match id associated to account
                    json_path = "summoner_matches/{0}/{1}/{2}.json".format(rank, division, summoner_id)
                    json_file = json.dumps(summoner, indent=4)
                    with open(json_path, "w") as file:
                        file.write(json_file)

    def load_high_elo_matches(self):
        """
        Function to load the match ids of the last 100 games for each account
        in high elo (challenger, grandmaster, master).
        """
        for rank in self.high_elo:

            path = "summoner_matches/{0}".format(rank)
            if not os.path.exists(path):
                os.makedirs(path)
            print("Generating matches for {0}".format(rank))
            file_path = "accounts/{0}.csv".format(rank)

            # Read account data
            accounts = pd.read_csv(file_path)
            for index, row in accounts.iterrows():

                summoner_id = row["summonerId"]
                summoner_api = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/{0}?api_key={1}".format(summoner_id, self._riot_api)
                response = requests.get(summoner_api)
                while response.status_code == 429:
                    time.sleep(10)
                    response = requests.get(summoner_api)
                summoner = response.json()

                puuid = summoner["puuid"]
                matches_api = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?type=ranked&count=100&api_key={1}".format(puuid, self._riot_api)
                response = requests.get(matches_api)
                while response.status_code == 429:
                    time.sleep(10)
                    response = requests.get(matches_api)
                matches = response.json()

                summoner["rank"] = row["rank"]
                summoner["wins"] = row["wins"]
                summoner["losses"] = row["losses"]
                summoner["matches"] = matches

                # Write match id associated to account
                json_path = "summoner_matches/{0}/{1}.json".format(rank, summoner_id)
                json_file = json.dumps(summoner, indent=4)
                with open(json_path, "w") as file:
                    file.write(json_file)

    def general_stats(self):
        """
        Function to load the winrate stats for each division.
        """
        # DIAMOND to IRON
        for rank in self.ranks:
            for division in self.divisions:

                file_path = "accounts/{0}_{1}.csv".format(rank, division)
                curr_rank = pd.read_csv(file_path)

                self.winrates[rank_division] = {}
                curr_rank['avg_win'] = curr_rank['wins'] / (curr_rank['losses'] + curr_rank['wins'])
                info = curr_rank['avg_win'].describe()
                rank_division = "{0}_{1}".format(rank, division)
                for key in info.keys():
                    self.winrates[rank_division][key] = info[key]

        # HIGH ELO
        for rank in self.high_elo:

            file_path = "accounts/{0}.csv".format(rank)
            curr_rank = pd.read_csv(file_path)
            
            self.winrates[rank] = {}
            curr_rank['avg_win'] = curr_rank['wins'] / (curr_rank['losses'] + curr_rank['wins'])
            info = curr_rank['avg_win'].describe()
            for key in info.keys():
                self.winrates[rank][key] = info[key]

        # Write data
        winrates_json = json.dumps(self.winrates, indent=4)
        with open("winrates.json", "w") as file:
            file.write(winrates_json)
    
    def load_general_match_data(self):
        """
        Function to load the match data of the past 100 games for each account
        between DIAMOND and IRON.
        """
        for rank in self.ranks:
            for division in self.divisions:

                path = "match_data/{0}/{1}".format(rank, division)
                if not os.path.exists(path):
                    os.makedirs(path)
                print("Generating match data for {0} {1}".format(rank, division))
                file_path = "summoner_matches/{0}/{1}".format(rank, division)

                # Get accounts and match ids
                for account in os.listdir(file_path):

                    account_path = "{0}/{1}".format(file_path, account)
                    with open(account_path, "r") as file:
                        account_matches = json.load(file)

                        match_path = "{0}/{1}".format(path, account_matches['puuid'])
                        if not os.path.exists(match_path):
                            os.makedirs(match_path)

                        # Get match data
                        for match in account_matches['matches']:

                            curr_match = "https://americas.api.riotgames.com/lol/match/v5/matches/{0}?api_key={1}".format(match, self._riot_api)
                            response = requests.get(curr_match)
                            while response.status_code == 429:
                                time.sleep(10)
                                response = requests.get(curr_match)
                            match_data = response.json()

                            # Write match data
                            json_path = "{0}/{1}.json".format(match_path, match)
                            json_file = json.dumps(match_data, indent=4)
                            with open(json_path, "w") as file:
                                file.write(json_file)       
    
    def load_high_elo_match_data(self):
        """
        Function to load the match data of the past 100 games for each account
        in high elo (challenger, grandmaster, master).
        """
        for rank in self.high_elo:

            path = "match_data/{0}".format(rank)
            if not os.path.exists(path):
                os.makedirs(path)
            print("Generating match data for {0}".format(rank))
            file_path = "summoner_matches/{0}".format(rank)

            # Get accounts and match ids
            count = 0
            for account in os.listdir(file_path):

                account_path = "{0}/{1}".format(file_path, account)
                with open(account_path, "r") as file:
                    account_matches = json.load(file)
                    if account_matches['wins'] + account_matches['losses'] > 200:

                        match_path = "{0}/{1}".format(path, account_matches['puuid'])
                        if not os.path.exists(match_path):
                            os.makedirs(match_path)

                        # Get match data
                        for match in account_matches['matches']:

                            curr_match = "https://americas.api.riotgames.com/lol/match/v5/matches/{0}?api_key={1}".format(match, self._riot_api)
                            response = requests.get(curr_match)
                            while response.status_code == 429:
                                time.sleep(10)
                                response = requests.get(curr_match)
                            match_data = response.json()

                            # Write match data
                            json_path = "{0}/{1}.json".format(match_path, match)
                            json_file = json.dumps(match_data, indent=4)
                            with open(json_path, "w") as file:
                                file.write(json_file)      
                        
                        count += 1
                        if count >= 100:
                            break              

    def verify_data(self):
        """
        Function to verify the data generated in all ranks 
        are not duplicates and is in the reference sample
        """
        # for rank in self.ranks:
        #     for division in self.divisions:

                # print("Verifying data for {0} {1}".format(rank, division))
                # account_path = "accounts/{0}_{1}.csv".format(rank, division)

                # accounts = pd.read_csv(account_path)
                # accounts = accounts['summonerId'].unique()
                # assert accounts.shape[0] == 100

        #         match_path = "match_data/{0}/{1}".format(rank, division)
        
        for rank in self.high_elo:

            print("Verifying data for {0}".format(rank))
            
            match_path = "match_data/{0}".format(rank)
            dic = {}
            for account in os.listdir(match_path):
                dic[account] = len(os.listdir(match_path + "/" + account))
            print(dict(sorted(dic.items(), key=lambda ky: ky[1])))
