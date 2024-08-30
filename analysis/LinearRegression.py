import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

data = {1: [0.6015686274509804, 3825], 2: [0.5381091211995002, 2401], 3: [0.5325289803643245, 1409], 4: [0.5383506343713956, 867], 5: [0.5069999999999999, 600], 6: [0.5324324324324324, 370], 7: [0.5162454873646208, 277], 8: [0.5013368983957219, 187], 9: [0.5250212044105175, 131], 10: [0.5211267605633803, 71], 11: [0.5164410058027079, 47], 12: [0.5023809523809525, 35], 13: [0.521978021978022, 28], 14: [0.43197278911564624, 21], 15: [0.5, 12], 16: [0.53125, 12], 17: [0.4764705882352941, 10], 18: [0.3968253968253968, 7], 19: [0.631578947368421, 1], 20: [0.5, 1], 21: [0.47619047619047616, 1], 22: [0.4090909090909091, 1], 27: [0.5185185185185185, 1], 28: [0.35714285714285715, 1], 34: [0.4411764705882353, 1]}

df = pd.DataFrame.from_dict(data, orient='index', columns=['Win Percentage', 'Occurrences'])
df.index.name = 'Games in Session'
df.reset_index(inplace=True)

# Prepare data for regression
X = df[['Games in Session']]  # Independent variable
y = df['Win Percentage']      # Dependent variable
weights = df['Occurrences']   # Weights based on occurrences

# Initialize and fit the linear regression model
model = LinearRegression()
model.fit(X, y, sample_weight=weights)

# Make predictions
y_pred = model.predict(X)

# Calculate metrics
mse = mean_squared_error(y, y_pred, sample_weight=weights)
r2 = r2_score(y, y_pred, sample_weight=weights)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Plot results
plt.figure(figsize=(10, 6))
plt.scatter(df['Games in Session'], df['Win Percentage'], color='blue', label='Data (scales with occurences)', s=weights)  # Size based on occurrences
plt.plot(df['Games in Session'], y_pred, color='red', linewidth=2, label='Fitted Line')
plt.xlabel('Games in Session')
plt.ylabel('Win Percentage')
plt.title('Weighted Linear Regression: Win Percentage vs. Games in Session')
plt.legend(loc='upper right', scatterpoints=1, markerscale=0.25, fontsize='medium', frameon=True)
plt.grid(True)
plt.show()