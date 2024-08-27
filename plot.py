import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
divisions = ["I", "II", "III", "IV"]
high_elo = ["challengerleagues", "grandmasterleagues", "masterleagues"]
rank_div = [[f"{rank}/{division}" for division in divisions] for rank in ranks]

def session():
    path = "session_winrates.json"
    sessions = pd.read_json(path)
    total = {}
    for i in range(13):
        total[i] = [0, 0]
    for index, row in sessions.iterrows():
        for rank in high_elo:
            total[index][0] += row[rank][0]
            total[index][1] += row[rank][1]
        for rank in ranks:
            for division in divisions:
                total[index][0] += row[f"{rank}/{division}"][0]
                total[index][1] += row[f"{rank}/{division}"][1]

    for i in range(13):
        total[i] = round(total[i][0] / (total[i][0] + total[i][1]), ndigits=3)
    total['12+']= total.pop(12)

    sessions = pd.DataFrame.from_dict(total, orient='index')
    sessions.index.name = "Number of games played"
    ax = sessions.plot.bar(ylim=(0.45, 0.535), ylabel="Winrate")

    for container in ax.containers:
        ax.bar_label(container)
    ax.get_legend().remove()
    plt.show()

def breaks():
    path = "breaks.json"
    breaks = pd.read_json(path)
    total = [0, 0]
    for rank in high_elo:
        total[0] += breaks[rank]['wins']
        total[1] += breaks[rank]['losses']
    for rank in ranks:
        for division in divisions:
            total[0] += breaks[f"{rank}/{division}"]['wins']
            total[1] += breaks[f"{rank}/{division}"]['losses']
    print(total[0] / (total[0] + total[1]))

def streaks():
    path = "streaks_winrates.json"
    streaks = pd.read_json(path)

    total = {}
    for i in range(3, 11):
        total[i] = [0, 0, 0, 0]
    for index, row in streaks.iterrows():
        for rank in high_elo:
            total[index][0] += row[rank]['0'][0]
            total[index][1] += row[rank]['0'][1]
            total[index][2] += row[rank]['1'][0]
            total[index][3] += row[rank]['1'][1]
        for rank in ranks:
            total[index][0] += row[rank]['0'][0]
            total[index][1] += row[rank]['0'][1]
            total[index][2] += row[rank]['1'][0]
            total[index][3] += row[rank]['1'][1]

    for i in range(3, 11):
        total[i] = [round(total[i][0] / (total[i][0] + total[i][1]), ndigits=3), round(total[i][2] / (total[i][2] + total[i][3]), ndigits=3)]
    total["10+"] = total.pop(10)

    sessions = pd.DataFrame.from_dict(total, orient='index')
    sessions.index.name = "Streak length"
    ax = sessions.plot.bar(ylim=(0.4, 0.70), ylabel="Winrate")

    for container in ax.containers:
        ax.bar_label(container)
    ax.get_legend().remove()
    plt.show()

def opt_session():
    path = "opt_session.json"
    session = pd.read_json(path)
    total = {}
    for i in range(1, 13):
        total[i] = [0, 0]
    for index, row in session.iterrows():
        for rank in high_elo:
            total[index][0] += row[rank][0]
            total[index][1] += row[rank][1]
    print(total)
    sum_total = 0
    for i in range(1, 13):
        sum_total += session['challengerleagues'][i][0] + session['challengerleagues'][i][1]
    print(sum_total)
    
opt_session()