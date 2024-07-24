import requests
import os
from dotenv import load_dotenv

load_dotenv()
riot_api = os.environ["RIOT_API"]
api_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/PositivityArc/pck"

api_url = api_url + "?api_key=" + riot_api
print(api_url)
response = requests.get(api_url)
player_info = response.json()

puuid = player_info['puuid']
matches_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/Q_iDlzDMhwd5XDZIMsbPnhrd68wp9r68WxFXESmJYZtCcsopxEFP2TH-Awn4gC7IoYf0fNW0eVktZg/ids?start=0&count=100"
matches_url = matches_url + "&api_key=" + riot_api
print(matches_url)
response = requests.get(matches_url)
matches = response.json()
print(matches)
