import pandas as pd

import sklearn

from sklearn.linear_model import LinearRegression

import sqlite3

from sklearn.impute import SimpleImputer


database_connection = sqlite3.connect('PlayerStats.db')

query = "SELECT * FROM Premier_League"

player_data = pd.read_sql(query, database_connection)

filtered_by_position = player_data.query("POSITION == 'Centre-Back'")

X = filtered_by_position[list(filtered_by_position)[3:]]
y = filtered_by_position[['MARKET_VALUE']]

imputer = SimpleImputer(strategy='constant', fill_value=0)
X = imputer.fit_transform(X)

linear_regression = LinearRegression(fit_intercept = True)
linear_regression.fit(X, y)

prediction = linear.predict(X)

filtered_by_position["PREDICTED_PRICE"] = prediction
filtered_by_position["DIFFERENCE"] = filtered_by_position["PREDICTED_PRICE"]-filtered_by_position["MARKET_VALUE"]

sorted_by_difference = filtered_by_position.sort_values(["DIFFERENCE"])
print(sorted_by_difference[['NAME', 'DIFFERENCE']].tail(5))
