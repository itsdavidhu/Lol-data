import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

data = {1: [0.6015686274509804, 3825], 2: [0.5381091211995002, 4802], 3: [0.5325289803643245, 4227], 4: [0.5383506343713956, 3468], 5: [0.5069999999999999, 3000], 6: [0.5324324324324324, 2220], 7: [0.5162454873646208, 1939], 8: [0.5013368983957219, 1496], 9: [0.5250212044105175, 1179], 10: [0.5211267605633803, 710], 11: [0.5164410058027079, 517], 12: [0.5023809523809525, 420], 13: [0.521978021978022, 364], 14: [0.43197278911564624, 364], 15: [0.5, 180], 16: [0.53125, 192], 17: [0.4764705882352941, 170], 18: [0.3968253968253968, 126], 19: [0.631578947368421, 19], 20: [0.5, 20], 21: [0.47619047619047616, 21], 22: [0.4090909090909091, 22], 27: [0.5185185185185185, 27], 28: [0.35714285714285715, 28], 34: [0.4411764705882353, 34]}

df = pd.DataFrame.from_dict(data, orient='index', columns=['Win Percentage', 'Occurrences'])
df.index.name = 'Games in Session'
df.reset_index(inplace=True)

# Prepare data for regression
X = df[['Games in Session']]  # Independent variable
y = df['Win Percentage']      # Dependent variable
weights = df['Occurrences']   # Weights based on occurrences

# Split data into train and test sets
X_train, X_test, y_train, y_test, weights_train, weights_test = train_test_split(X, y, weights, test_size=0.3, random_state=42)

poly = PolynomialFeatures(degree=5)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Fit model with weights
model = LinearRegression()
model.fit(X_train_poly, y_train, sample_weight=weights_train)

# Predict
y_train_pred = model.predict(X_train_poly)
y_test_pred = model.predict(X_test_poly)

# Evaluate

print("Test MSE:", mean_squared_error(y_test, y_test_pred, sample_weight=weights_test))
print("Test R^2:", r2_score(y_test, y_test_pred, sample_weight=weights_test))

plt.figure(figsize=(10, 6))
plt.scatter(X, y, s=weights, color='blue', alpha=0.5, label='Data')
X_fit = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
X_fit_poly = poly.transform(X_fit)
y_fit = model.predict(X_fit_poly)
plt.plot(X_fit, y_fit, color='red', label='Weighted Polynomial fit (degree=5)')
plt.xlabel('Session Length')
plt.ylabel('Win Rate')
plt.title('Weighted Polynomial Regression: Win Percentage vs. Games in Session (Master - Challenger)')
plt.legend(loc='upper right', scatterpoints=1, markerscale=0.25, fontsize='medium', frameon=True)
plt.show()