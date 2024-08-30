import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = {
    1: [0.6015686274509804, 3825],
    2: [0.5381091211995002, 2401],
    3: [0.5325289803643245, 1409],
    4: [0.5383506343713956, 867],
    5: [0.5069999999999999, 600],
    6: [0.5324324324324324, 370],
    7: [0.5162454873646208, 277],
    8: [0.5013368983957219, 187],
    9: [0.5250212044105175, 131],
    10: [0.5211267605633803, 71],
    11: [0.5164410058027079, 47],
    12: [0.5023809523809525, 35],
    13: [0.521978021978022, 28],
    14: [0.43197278911564624, 21],
    15: [0.5, 12],
    16: [0.53125, 12],
    17: [0.4764705882352941, 10],
    18: [0.3968253968253968, 7],
    19: [0.631578947368421, 1],
    20: [0.5, 1],
    21: [0.47619047619047616, 1],
    22: [0.4090909090909091, 1],
    27: [0.5185185185185185, 1],
    28: [0.35714285714285715, 1],
    34: [0.4411764705882353, 1]
}

# Convert data to a DataFrame
df = pd.DataFrame.from_dict(data, orient='index', columns=['Win Percentage', 'Occurrences'])
df.index.name = 'Length of Session'
df.reset_index(inplace=True)

# Create the scatter plot
plt.figure(figsize=(14, 8))
plt.scatter(df['Length of Session'], df['Win Percentage'], s=df['Occurrences'], alpha=0.6, edgecolors='w', linewidth=0.5)
plt.xlabel('Length of Session')
plt.ylabel('Win Percentage')
plt.title('Win Percentage vs. Length of Session')
plt.grid(True)
plt.show()