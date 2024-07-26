import requests
import os
from dotenv import load_dotenv
import csv

load_dotenv()
riot_api = os.environ["RIOT_API"]
ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
divisions = ["I", "II", "III", "IV"]

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


# account_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/PositivityArc/pck"
# account_url = account_url + "?api_key=" + riot_api
# response = requests.get(account_url)
# player_info = response.json()
# puuid = player_info['puuid']

# matches_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=100"
# matches_url = matches_url + "&api_key=" + riot_api
# response = requests.get(matches_url)
# matches = response.json()

# for match in matches:
#     match_api = "https://americas.api.riotgames.com/lol/match/v5/matches/" + match + "?api_key=" + riot_api
#     response = requests.get(match_api)
#     match_data = response.json()

