import os
import pandas as pd
import json

ranks = ["masterleagues", "grandmasterleagues", "challengerleagues", "DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
divisions = ["I", "II", "III", "IV"]
winrates = {}

for rank in ranks:
    if rank.endswith("leagues"):
        file_path = "accounts/{0}.csv".format(rank)
        curr_rank = pd.read_csv(file_path)
        curr_rank['avg_win'] = curr_rank['wins'] / (curr_rank['losses'] + curr_rank['wins'])
        winrates[rank] = curr_rank['avg_win'].median()
    else:
        for division in divisions:
            file_path = "accounts/{0}_{1}.csv".format(rank, division)
            curr_rank = pd.read_csv(file_path)
            curr_rank['avg_win'] = curr_rank['wins'] / (curr_rank['losses'] + curr_rank['wins'])
            winrates["{0}_{1}".format(rank, division)] = curr_rank['avg_win'].median()
winrates_json = json.dumps(winrates, indent=4)
with open("winrates.json", "w") as file:
    file.write(winrates_json)