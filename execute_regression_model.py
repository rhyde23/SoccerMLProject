#Executing the Regression Model to identify overvalued/undervalued players

#Import pandas library to load dataframes
import pandas as pd

#Import sklearn library to perform ML models
import sklearn

#Import the LinearRegression class from sklearn to perform a linear regression
from sklearn.linear_model import LinearRegression

#Import sqlite3 module to establish connection to PlayerStats.db
import sqlite3

#Import the SimpleImputer class from sklearn to replace all null values with 0
from sklearn.impute import SimpleImputer

groups_of_similar_positions = [
    ['Centre-Forward'],
    ['Right Winger', 'Left Midfield', 'Right Midfield', 'Left Winger'],
    ['Central Midfield'],
    ['Defensive Midfield'],
    ['Attacking Midfield', 'Second Striker'],
    ['Left-Back', 'Right-Back'],
    ['Centre-Back']
]

def build_query(group_of_similar_positions) :
    
    return "SELECT * FROM "+table_name+" WHERE POSITION == 'Centre-Back' OR POSITION == 'Right-Back'"


def perform_regressions_on_league(table_name) :
    
    #Connect to the Player Stats Database
    database_connection = sqlite3.connect('PlayerStats.db')

    #Query to select all data from a given table
    query = "SELECT * FROM "+table_name#+" WHERE POSITION == 'Centre-Back' OR POSITION == 'Right-Back'"

    #Read the SQL table and store into "player_data" using pandas' function read_sql
    player_data = pd.read_sql(query, database_connection)

    #Filter by

    print(player_data["POSITION"].unique())
    #quit()
    
    #filtered_by_position = player_data.query("POSITION == 'Centre-Back' OR POSITION == 'Right-Back' ")
    """
    print(player_data)
    quit()
    
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
    """

