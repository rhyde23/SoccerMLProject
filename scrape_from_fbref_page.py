#Scraping script

#Import requests library for requests for html content of websites 
import requests

#Import unidecode for removing accents from letters in strings
from unidecode import unidecode

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#The "goalkeeper_tables_to_scrape" dictionary contains all of the relevant tables for data scraping and which stats from those tables are of interest for Goalkeepers 
goalkeeper_tables_to_scrape = {
    "Goalkeeping":['Age', 'Goals Against/90', 'Save Percentage', 'Clean Sheet Percentage', 'Save% (Penalty Kicks)'],
    "Advanced Goalkeeping":['PSxG/SoT'],
}

#The "tables_to_scrape" dictionary contains all of the relevant tables for data scraping and which stats from those tables are of interest for non-Goalkeepers 
tables_to_scrape = {
    "Shooting":['Age', 'Goals', 'Shots on Target %', 'Shots Total/90', 'Shots on target/90', 'Goals/Shot', 'Goals/Shot on Target', 'xG: Expected Goals', 'npxG: Non-Penalty xG'],
    "Passing":['Pass Completion %', 'Pass Completion % (Short)', 'Pass Completion % (Medium)', 'Pass Completion % (Long)', 'Assists', 'xAG: Exp. Assisted Goals', 'xA: Expected Assists', 'Key Passes', 'Progressive Passes'],
    "Goal and Shot Creation":['Shot-Creating Actions/90', 'Goal-Creating Actions/90'],
    "Defensive Actions":['Tackles Won', '% of Dribblers Tackled', 'Blocks', 'Shots Blocked', 'Passes Blocked', 'Interceptions', 'Clearances'],
    "Possession":['Successful Take-On %', 'Carries', 'Progressive Carries', 'Carries into Final Third', 'Carries into Penalty Area'],
    "Miscellaneous Stats":['% of Aerials Won'],
}

#The "convert_string_to_sql_column_name" function takes an FBRef column name and makes it SQL-friendly
def convert_string_to_sql_column_name(name) :

    #Get rid of unique characters and spaces, and make everything uppercase
    return name.replace(" ", "_").replace("%", "PERCENT").replace("/", "_PER_").replace("Exp.", "EXPECTED").replace(":", "").replace("-", "_").replace("(", "").replace(")", "").upper()

#The "get_database_column_names" function gets all of the column names for the Database from the "tables_to_scrape" dictionary that contains all the FBRef column names
def get_database_column_names() :

    #The "tables_in_order" list contains the keys of "tables_to_scrape" in the correct order
    tables_in_order = ["Shooting", "Passing", "Goal and Shot Creation", "Defensive Actions", "Possession", "Miscellaneous Stats"]

    #The "gk_tables_in_order" list contains the keys of "goalkeeper_tables_to_scrape" in the correct order 
    gk_tables_in_order = ["Goalkeeping", "Advanced Goalkeeping"]

    #The "sql_names" list will be populated with all the converted names for non-GK's
    sql_names = []

    #The "gk_sql_names" list will be populated with all the converted names for GK's
    gk_sql_names = []

    #Iterate through table name in "tables_in_order"
    for table in tables_in_order :

        #Add the converted names from this table to "sql_names"
        sql_names = sql_names + [convert_string_to_sql_column_name(column_name) for column_name in tables_to_scrape[table]]

    #Iterate through table name in "gk_tables_in_order"
    for table in gk_tables_in_order :

        #Add the converted names from this table to "gk_sql_names"
        gk_sql_names = gk_sql_names + [convert_string_to_sql_column_name(column_name) for column_name in goalkeeper_tables_to_scrape[table]]

    #Return "sql_names" and "gk_sql_names"
    return sql_names, gk_sql_names

#The "ninetys_played_minimum" float is the minimum amount of 90s played for a player to be included in the dataset
ninetys_played_minimum = 5

#The "get_all_aria_labels" function simply returns a list of all the stats present in a data table (for development purposes)
def get_all_aria_labels(headers_row) :

    #Return a list of each aria-label for each header in the row of headers
    return [header["aria-label"] for header in headers_row.find_all("th")]

#The "convert_to_float_or_none" function converts a string to either a float or None type if empty string
def convert_to_float_or_none(x) :
    try :
        return float(x)
    except :
        pass

#The "scrape_row" function scrapes all the content from a row
def scrape_row(row, header_indexes) :

    #The "player_name" string is the name of the player in this row, with accents removed.
    player_name = unidecode(row.find("th").text)

    #Return the player name, and a list of each data point that is of interest based on the "header_indexes" list, which is derived from the "tables_to_scrape" dictionary
    return player_name, [convert_to_float_or_none(data_point.text) for data_point_index, data_point in enumerate(row.find_all("td")) if data_point_index in header_indexes]

#The "scrape_headers_row" function returns a list of indexes of data points that are desired from a table
def scrape_headers_row(headers_row, desired_data_points) :

    #Return the list of indexes such that the aria-label of the header for this column is in the "desired_data_points" list
    return [header_index for header_index, header in enumerate(headers_row.find_all("th")[1:]) if header["aria-label"] in desired_data_points]

#The "scrape_table" function scrapes all the content from a table
def scrape_table(table, season, players, goalkeepers) :

    #The "caption" string is the caption of the table
    caption = table.find("caption").text.split(season)[0][:-1]

    #The "goalkeeper" boolean indicates whether the player is a goalkeeper
    goalkeeper = False

    #If the table caption is within "goalkeeper_tables_to_scrape" dictionary 
    if caption in goalkeeper_tables_to_scrape :

        #Set "goalkeeper" boolean to True
        goalkeeper = True

        #The "rows_to_scrape" list from the "goalkeeper_tables_to_scrape" contains all the column names of stats that I care about
        rows_to_scrape = goalkeeper_tables_to_scrape[caption]
    else :
        #If the caption is not within the relevant tables, return None
        if not caption in tables_to_scrape :
            return None

        #The "rows_to_scrape" list from the "tables_to_scrape" contains all the column names of stats that I care about
        rows_to_scrape = tables_to_scrape[caption]

    #The "all_rows" list is the list of row bs4 classes from this table
    all_rows = table.find_all("tr")

    #The "headers_row" class is the second row of the table, which contains all the names of each data point present in this table
    headers_row = all_rows[1]

    #The "header_indexes" list is the list of indexes for each desired data point
    header_indexes = scrape_headers_row(headers_row, rows_to_scrape)

    #Loop through each row in the table (besides the first two rows, which are header rows)
    for row in all_rows[2:] :

        #If the player's 90's played stat is greater or equal to "ninetys_played_minimum"
        if float(row.find('td', {"data-stat": 'minutes_90s'}).text) >= ninetys_played_minimum :

            #Call the "scrape_row" function to scrape the content of this row
            player_name, row_data = scrape_row(row, header_indexes)
        
            #If the table's caption pertains to goalkeepers 
            if goalkeeper :

                #If the player's name is not already a key in "goalkeepers" dict
                if not player_name in goalkeepers :

                    #Set the value for "player_name" in the "goalkeepers" dict as the "row_data" list
                    goalkeepers[player_name] = row_data

                #If the player's name is already in the "goalkeepers" dict
                else :

                    #Set the value for "player_name" in the "goalkeepers" dict as itself plus the "row_data" list 
                    goalkeepers[player_name] = goalkeepers[player_name]+row_data

            #If the table's caption does not pertain to goalkeepers 
            else :

                #If the player's name is not already in goalkeepers (because goalkeepers appear in the Passing table, for example)
                if not player_name in goalkeepers :

                    #If the player's name is not already a key in "players" dict
                    if not player_name in players :

                        #Set the value for "player_name" in the "players" dict as the "row_data" list
                        players[player_name] = row_data

                    #If the player's name is already in the "players" dict
                    else :

                        #Set the value for "player_name" in the "players" dict as itself plus the "row_data" list 
                        players[player_name] = players[player_name]+row_data
#The "remove_totals" function removes the "Squad Total" and "Opponent Total" in a stats dictionary if they are present    
def remove_totals(stats) :

    #If the key "Squad Total" is in the dictionary
    if "Squad Total" in stats :

        #Delete the entry 
        del stats["Squad Total"]

    #If the key "Opponent Total" is in the dictionary
    if "Opponent Total" in stats :

        #Delete the entry 
        del stats["Opponent Total"]
    
#The "scrape" function scrapes all the content from a team page
def scrape(url) :

    #The "goalkeepers" and the "players" dictionaries will contain all the stats for each goalkeeper and non-goalkeeper, respectively
    goalkeepers, players = {}, {}

    #The "request" object is the html content from the given url
    request = requests.get(url)

    #The "soup" object is the beautiful soup object we will call .find() and .find_all() for certain tags and extract their text
    soup = BeautifulSoup(request.content, "html.parser")

    #The "season" string is the season for these stats found at the header of the page. Example: "2023-24"
    season = soup.find("h1").text.split(" ")[0][1:]

    #Loop through each table in the page
    for table in soup.find_all("table") :

        #Call the "scrape_table" function to scrape the content of this table
        scrape_table(table, season, players, goalkeepers)

    #Call "remove_totals" for "players"
    remove_totals(players)

    #Call "remove_totals" for "goalkeepers"
    remove_totals(goalkeepers)

    #Return the "players" and "goalkeepers" dictionaries.
    return players, goalkeepers
