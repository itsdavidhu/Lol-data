import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import numpy as np

ranks = ["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
divisions = ["I", "II", "III", "IV"]
high_elo = ["challengerleagues", "grandmasterleagues", "masterleagues"]
rank_div = [[f"{rank}/{division}" for division in divisions] for rank in ranks]

def session():
    path = "data/session_winrates.json"
    sessions = pd.read_json(path)

    # high_elo_total = {}
    # for i in range(13):
    #     high_elo_total[i] = [0, 0]

    # for index, row in sessions.iterrows():
    #     for rank in high_elo:
    #         high_elo_total[index][0] += row[rank][0]
    #         high_elo_total[index][1] += row[rank][1]

    # for i in range(13):
    #     high_elo_total[i] = round(high_elo_total[i][0] / (high_elo_total[i][0] + high_elo_total[i][1]), ndigits=3)
    # high_elo_total['12+']= high_elo_total.pop(12)

    # high_elo_graph = pd.DataFrame.from_dict(high_elo_total, orient='index')
    # high_elo_graph.index.name = "Number of games played before"
    # ax = high_elo_graph.plot.bar(ylim=(0.45, 0.60), ylabel="Winrate")

    # for container in ax.containers:
    #     ax.bar_label(container)

    # plt.title("Optimal Session Length - High Elo")
    # ax.get_legend().remove()
    # plt.show()

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
        total[i] = round(total[i][0] / (total[i][0] + total[i][1]), ndigits=3) * 100
    total['12+']= total.pop(12)

    general = pd.DataFrame.from_dict(total, orient='index')
    general.index.name = "Number of games played before"
    ax = general.plot.bar(ylabel="Winrate", ylim=(45, 53.5))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%')
    ax.get_legend().remove()
    plt.title("Next Game Winrates given Session Length - General")
    plt.show()

def breaks():
    path = "data/breaks.json"
    breaks = pd.read_json(path)
    total = [[0, 0], [0, 0]]
    for rank in high_elo:
        total[0][0] += breaks[rank][0][0]
        total[0][1] += breaks[rank][0][1]
        total[1][0] += breaks[rank][1][0]
        total[1][1] += breaks[rank][1][1]
    win_after_win = round(total[0][0] / (total[0][0] + total[0][1]), ndigits=3) * 100
    win_after_loss = round(total[1][0] / (total[1][0] + total[1][1]), ndigits=3) * 100
    print("Winrate after win given break in high elo: {0}%".format(win_after_win))
    print("Winrate after loss given break in high elo: {0}%".format(win_after_loss))
    for rank in ranks:
        for division in divisions:
            total[0][0] += breaks[f"{rank}/{division}"][0][0]
            total[0][1] += breaks[f"{rank}/{division}"][0][1]
            total[1][0] += breaks[f"{rank}/{division}"][1][0]
            total[1][1] += breaks[f"{rank}/{division}"][1][1]
    win_after_win = round(total[0][0] / (total[0][0] + total[0][1]), ndigits=3) * 100
    win_after_loss = round(total[1][0] / (total[1][0] + total[1][1]), ndigits=3) * 100
    print("Winrate after win given break: {0}%".format(win_after_win))
    print("Winrate after loss given break: {0}%".format(win_after_loss))

def streaks():
    path = "data/streaks_winrates.json"
    sessions = pd.read_json(path)

    # high_elo_total = {}
    # for i in range(3, 11):
    #     high_elo_total[i] = [0, 0, 0, 0]
    # for index, row in sessions.iterrows():
    #     for rank in high_elo:
    #         high_elo_total[index][0] += row[rank]['0'][0]
    #         high_elo_total[index][1] += row[rank]['0'][1]
    #         high_elo_total[index][2] += row[rank]['1'][0]
    #         high_elo_total[index][3] += row[rank]['1'][1]
    # for i in range(3, 11):
    #     high_elo_total[i] = [round(high_elo_total[i][0] / (high_elo_total[i][0] + high_elo_total[i][1]), ndigits=3), 
    #                          round(high_elo_total[i][2] / (high_elo_total[i][2] + high_elo_total[i][3]), ndigits=3)]
    # high_elo_total["10+"] = high_elo_total.pop(10)

    # high_elo_graph = pd.DataFrame.from_dict(high_elo_total, orient='index')
    # high_elo_graph.index.name = "Length of streak"
    # ax = high_elo_graph.plot.bar(ylim=(0.40, 0.65), ylabel="Winrate of next game")

    # for container in ax.containers:
    #     ax.bar_label(container)
    # plt.title("Optimal Streak Length - High Elo")
    # ax.get_legend().remove()
    # plt.show()

    total = {}
    for i in range(3, 11):
        total[i] = [0, 0, 0, 0]
    for index, row in sessions.iterrows():
        for rank in high_elo:
            total[index][0] += row[rank]['0'][0]
            total[index][1] += row[rank]['0'][1]
            total[index][2] += row[rank]['1'][0]
            total[index][3] += row[rank]['1'][1]
        for rank in ranks:
            for division in divisions:
                total[index][0] += row[f"{rank}/{division}"]['0'][0]
                total[index][1] += row[f"{rank}/{division}"]['0'][1]
                total[index][2] += row[f"{rank}/{division}"]['1'][0]
                total[index][3] += row[f"{rank}/{division}"]['1'][1]
    for i in range(3, 11):
        total[i] = [round(total[i][0] / (total[i][0] + total[i][1]), ndigits=3) * 100, round(total[i][2] / (total[i][2] + total[i][3]), ndigits=3) * 100]
    total["10+"] = total.pop(10)

    general = pd.DataFrame.from_dict(total, orient='index')
    general.index.name = "Length of streak"
    ax = general.plot.bar(ylim=(40, 65), ylabel="Winrate")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%')
    handles, labels = ax.get_legend_handles_labels()
    labels = ['Win Streak', 'Loss Streak']
    ax.legend(handles, labels)
    plt.title("Next Game Winrate given Length of streak - General")
    plt.show()

def opt_session():
    path = "data/opt_session.json"
    sessions = pd.read_json(path)

    high_elo_total = {}
    for i in range(1, 13):
        high_elo_total[i] = [0, 0]

    for index, row in sessions.iterrows():
        for rank in high_elo:
            high_elo_total[index][0] += row[rank][0]
            high_elo_total[index][1] += row[rank][1]

    for i in range(1, 13):
        high_elo_total[i] = round(high_elo_total[i][0] / (high_elo_total[i][0] + high_elo_total[i][1]), ndigits=3) * 100
    high_elo_total['12+']= high_elo_total.pop(12)

    high_elo_graph = pd.DataFrame.from_dict(high_elo_total, orient='index')
    high_elo_graph.index.name = "Number of games played in a session"
    ax = high_elo_graph.plot.bar(ylim=(45, 65), ylabel="Winrate")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%')

    plt.title("Winrate of Session given Total Number of Games Played - High Elo")
    ax.get_legend().remove()
    plt.show()

    total = {}
    for i in range(1, 13):
        total[i] = [0, 0]
    for index, row in sessions.iterrows():
        for rank in high_elo:
            total[index][0] += row[rank][0]
            total[index][1] += row[rank][1]
        for rank in ranks:
            for division in divisions:
                total[index][0] += row[f"{rank}/{division}"][0]
                total[index][1] += row[f"{rank}/{division}"][1]
    for i in range(1, 13):
        total[i] = round(total[i][0] / (total[i][0] + total[i][1]), ndigits=3) * 100
    total['12+']= total.pop(12)

    general = pd.DataFrame.from_dict(total, orient='index')
    general.index.name = "Number of games played in a session"
    ax = general.plot.bar(ylim=(45, 53.5), ylabel="Winrate")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%')
    ax.get_legend().remove()
    plt.title("Winrate of Session given Total Number of Games Played - General")
    plt.show()

session()
opt_session()
streaks()
breaks()
