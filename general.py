import requests
import os
from dotenv import load_dotenv

load_dotenv()
riot_api = os.environ["RIOT_API"]

account_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/PositivityArc/pck"
account_url = account_url + "?api_key=" + riot_api
response = requests.get(account_url)
player_info = response.json()
puuid = player_info['puuid']

matches_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=100"
matches_url = matches_url + "&api_key=" + riot_api
response = requests.get(matches_url)
matches = response.json()

for match in matches:
    match_api = "https://americas.api.riotgames.com/lol/match/v5/matches/" + match + "?api_key=" + riot_api
    response = requests.get(match_api)
    match_data = response.json()