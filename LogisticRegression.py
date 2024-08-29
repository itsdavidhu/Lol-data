import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score
import matplotlib.pyplot as plt
data = {
    "challengerleagues": {
        "1": [828, 492],
        "2": [898, 720],
        "3": [777, 594],
        "4": [670, 546],
        "5": [546, 509],
        "6": [420, 360],
        "7": [343, 308],
        "8": [224, 200],
        "9": [183, 150],
        "10": [138, 122],
        "11": [108, 90],
        "12": [366, 336]
    },
    "grandmasterleagues": {
        "1": [772, 487],
        "2": [851, 701],
        "3": [723, 690],
        "4": [613, 491],
        "5": [446, 484],
        "6": [368, 328],
        "7": [361, 318],
        "8": [298, 302],
        "9": [292, 257],
        "10": [116, 124],
        "11": [105, 104],
        "12": [344, 358]
    },
    "masterleagues": {
        "1": [715, 546],
        "2": [879, 825],
        "3": [772, 716],
        "4": [614, 582],
        "5": [531, 489],
        "6": [430, 404],
        "7": [326, 325],
        "8": [285, 299],
        "9": [142, 155],
        "10": [120, 110],
        "11": [46, 53],
        "12": [277, 306]
    }
}
rows = []
for league, sessions in data.items():
    for session_length, outcomes in sessions.items():
        wins, losses = outcomes
        for _ in range(wins):
            rows.append([int(session_length), 1, league])
        for _ in range(losses):
            rows.append([int(session_length), 0, league])

df = pd.DataFrame(rows, columns=["session_length", "win", "league"])

X = df[['session_length']]  # Independent variable(s)
y = df['win']               # Dependent variable

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Fit the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))

coefficients = model.coef_
odds_ratios = np.exp(coefficients)
print("Coefficients:", coefficients)
print("Odds Ratios:", odds_ratios)
