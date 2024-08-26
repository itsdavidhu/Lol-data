import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def winrate(games):
    return games[0] / (games[0] + games[1])

ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
divisions = ["I", "II", "III", "IV"]
rank_div = [[f"{rank}/{division}" for division in divisions] for rank in ranks]

path = "session_winrates.json"
sessions = pd.read_json(path)
sessions = sessions.map(lambda x: winrate(x))
for i in range(len(ranks)):
    sessions[ranks[i]] = sessions[rank_div[i]].mean(axis=1)
    sessions = sessions.drop(rank_div[i], axis=1)

sessions = sessions.mean(axis=1)

sessions.plot.bar(ylim=(0.45, 0.55), xlabel="Number of games played in a session", ylabel="Winrate")
ax = sessions.plot.bar()

for container in ax.containers:
    ax.bar_label(container)
plt.show()