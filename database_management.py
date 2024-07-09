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

    gk_table_name = table_name+"_GK"

    #Build the query including NAME, POSITION, MARKET_VALUE and all the FBRef column names 
    query = f"""CREATE TABLE {table_name} (NAME VARCHAR(255), POSITION VARCHAR(255), MARKET_VALUE int, """+fbref_column_names_query+""");"""

    gk_query = f"""CREATE TABLE {gk_table_name} (NAME VARCHAR(255), POSITION VARCHAR(255), MARKET_VALUE int, """+fbref_gk_column_names_query+""");"""

    #Return the query string
    return query, gk_query
    

#The "create_tables" function creates a table within PlayerStats for non-GK's and GK's of this league
def create_tables(table_name) :

    query, gk_query = build_create_table_querys(table_name)
    
    #Use the CREATE query to create the table 
    cursor.execute(query)

    cursor.execute(gk_query)

#The "enter_player_in_database" function enters a player within a league database table as a row in the table.
def enter_player_in_database(table_name, player_name, player_position, player_mv, player_stats) :

    row = tuple([player_name, player_position, player_mv]+player_stats)

    print(row)
    
    question_mark_string = "("+",".join(["?"]*len(row))+")"
    
    cursor.execute(f"""INSERT INTO {table_name} VALUES """+question_mark_string, row)

    #Commit changes
    database_connection.commit()

    print(player_name, "committed")

def close_connection() :

    #Close connection
    database_connection.close()
    
#close_connection()
