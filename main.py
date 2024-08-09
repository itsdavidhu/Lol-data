from lol_data import LolData

lol_data = LolData()
lol_data.load_general_accounts()
lol_data.verify_data()
lol_data.load_high_elo_accounts()
lol_data.load_general_matches()
lol_data.load_high_elo_matches()
lol_data.load_general_match_data()
lol_data.load_high_elo_match_data()