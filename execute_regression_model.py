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

#The "groups_of_similar_positions" groups similar positions in each list
groups_of_similar_positions = [
    ['Centre-Forward'],
    ['Right Winger', 'Left Midfield', 'Right Midfield', 'Left Winger'],
    ['Central Midfield'],
    ['Defensive Midfield'],
    ['Attacking Midfield', 'Second Striker'],
    ['Left-Back', 'Right-Back'],
    ['Centre-Back']
]

#The "build_query" function builds the query to select only the players from the desired similar position group
def build_query(table_name, group_of_similar_positions) :

    #Build the conditional part of the query by joining each position in the group with " OR "
    query_conditional = " OR ".join(["POSITION == \'"+position+"\'" for position in group_of_similar_positions])

    #Return the Select all From part of the query and the table name with the conditional part added on the end
    return "SELECT * FROM "+table_name+" WHERE "+query_conditional

#The "perform_regressions_on_league" function performs the linear regression on each group of similar positions
def perform_regressions_on_league(table_name) :
    
    #Connect to the Player Stats Database
    database_connection = sqlite3.connect('PlayerStats.db')

    #Iterate through each similar position group to perform the regression.
    for group_of_similar_positions in groups_of_similar_positions :

        #Query to select all data from a given table
        query = build_query(table_name, group_of_similar_positions)

        #Read the SQL table and store into "player_data" using pandas' function read_sql
        player_data = pd.read_sql(query, database_connection)

        #Set the input data as every column except for name, position, and marke value
        X = player_data[list(player_data)[3:]]

        #Set the output data as market value
        y = player_data[['MARKET_VALUE']]

        #Get rid of all null values and replace with 0
        imputer = SimpleImputer(strategy='constant', fill_value=0)
        X = imputer.fit_transform(X)

        #Create the "linear_regression" object
        linear_regression = LinearRegression(fit_intercept = True)

        #Fit the refression line to the data
        linear_regression.fit(X, y)

        #Make the predicted prices using the fit linear regression
        prediction = linear_regression.predict(X)

        #Store these predicted prices in "PREDICTED_PRICE"
        player_data["PREDICTED_PRICE"] = prediction

        #Store the ratio of each player's predicted price divided by their real market value in "DIFFERENCE_PERCENTAGE"
        player_data["DIFFERENCE_PERCENTAGE"] = player_data["PREDICTED_PRICE"]/player_data["MARKET_VALUE"]

        #Sort the player data by this difference percentage
        sorted_by_difference = player_data.sort_values(["DIFFERENCE_PERCENTAGE"])

        #Print the 10 most undervalued players in this position group for this league
        print(sorted_by_difference[['NAME', 'DIFFERENCE_PERCENTAGE']].tail(10))
        
        print()
        print()
        print()

