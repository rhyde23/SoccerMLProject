#Database Management
import sqlite3

#Import the "get_database_column_names" function from "scrape_from_fbref_page"
from scrape_from_fbref_page import get_database_column_names

#Connect to the Player Stats Database
database_connection = sqlite3.connect('PlayerStats.db')

#The "cursor" object allows editing of the database
cursor = database_connection.cursor()

#The "table_exists" function check if a table name exists in PlayerStats
def table_exists(table_name) :

    #Return the boolean if this Select query is not an empty array (or if the query returns something)
    return cursor.execute(
  f"""SELECT name FROM sqlite_master WHERE type='table'
  AND name='{table_name}'; """).fetchall() != []

#The "build_create_table_query" function builds two querys to create Database tables based on the desired column names from FBRef scraping for non-GK's and GK's 
def build_create_table_querys(table_name) :

    #Call the "get_database_column_names" function from "scrape_from_fbref_page" to get all the FBRef statistic column names in a SQL-friendly format for non-GK's and GK's.
    fbref_column_names, fbref_gk_column_names = get_database_column_names()

    #Join all the column names using " int, " to build the FBRef column part of the query
    fbref_column_names_query, fbref_gk_column_names_query = " int, ".join(fbref_column_names)+" int", " int, ".join(fbref_gk_column_names)+" int"

    #The "gk_table_name" string is the GK version of the table name by adding "_GK" to the end of it
    gk_table_name = table_name+"_GK"

    #Build the query for non-GK's including NAME, POSITION, MARKET_VALUE and all the FBRef column names 
    query = f"""CREATE TABLE {table_name} (NAME VARCHAR(255), POSITION VARCHAR(255), MARKET_VALUE int, """+fbref_column_names_query+""");"""

    #Build the query for GK's including NAME, POSITION, MARKET_VALUE and all the FBRef column names 
    gk_query = f"""CREATE TABLE {gk_table_name} (NAME VARCHAR(255), POSITION VARCHAR(255), MARKET_VALUE int, """+fbref_gk_column_names_query+""");"""

    #Return the two query strings
    return query, gk_query
    

#The "create_tables" function creates a table within PlayerStats for non-GK's and GK's of this league
def create_tables(table_name) :

    #Call the "build_create_table_querys" function to get the non-GK create table query and the GK create table query
    query, gk_query = build_create_table_querys(table_name)
    
    #Use the non-GK query to create the non-GK table 
    cursor.execute(query)

    #Use the GK CREATE query to create the GK table 
    cursor.execute(gk_query)

#The "enter_player_in_database" function enters a player within a league database table as a row in the table.
def enter_player_in_database(table_name, player_name, player_position, player_mv, player_stats) :

    #The "row" tuple will contain all the corresponding values for each column in the league table
    row = tuple([player_name, player_position, player_mv]+player_stats)

    #The "question_mark_string" is the SQL string (?,?,?,etc.) for how many values are in the row
    question_mark_string = "("+",".join(["?"]*len(row))+")"

    #Execute the INSERT function to insert this player's row in the league table
    cursor.execute(f"""INSERT INTO {table_name} VALUES """+question_mark_string, row)

    #Commit changes
    database_connection.commit()

    print(player_name, "committed")

#The "close_connection" function closes the connection to the SQL database
def close_connection() :

    #Close connection
    database_connection.close()
    
#close_connection()
