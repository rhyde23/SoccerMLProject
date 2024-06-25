#Scraping script

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#The "tables_to_scrape" dictionary contains all of the relevant tables for data scraping and which stats from those tables are of interest

goalkeeper_tables_to_scrape = {
    "Goalkeeping":['Age', 'Goals Against/90', 'Save Percentage', 'Clean Sheet Percentage', 'Save% (Penalty Kicks)'],
    "Advanced Goalkeeping":['PSxG/SoT'],
}

tables_to_scrape = {
    "Shooting":['Age', 'Goals', 'Shots on Target %', 'Shots Total/90', 'Shots on target/90', 'Goals/Shot', 'Goals/Shot on Target', 'xG: Expected Goals', 'npxG: Non-Penalty xG'],
    "Passing":['Pass Completion %', 'Pass Completion % (Short)', 'Pass Completion % (Medium)', 'Pass Completion % (Long)', 'Assists', 'xAG: Exp. Assisted Goals', 'xA: Expected Assists', 'Key Passes', 'Progressive Passes'],
    "Goal and Shot Creation":['Shot-Creating Actions/90', 'Goal-Creating Actions/90'],
    "Defensive Actions":['Tackles Won', '% of Dribblers Tackled', 'Blocks', 'Shots Blocked', 'Passes Blocked', 'Interceptions', 'Clearances'],
    "Possession":['Successful Take-On %', 'Carries', 'Progressive Carries', 'Carries into Final Third', 'Carries into Penalty Area'],
    "Miscellaneous Stats":['% of Aerials Won'],
}

ninetys_played_minimum = 5

goalkeepers, players = {}, {}

#The "get_all_aria_labels" function simply returns a list of all the stats present in a data table (for development purposes)
def get_all_aria_labels(headers_row) :

    #Return a list of each aria-label for each header in the row of headers
    return [header["aria-label"] for header in headers_row.find_all("th")]

def convert_to_float_or_none(x) :
    try :
        return float(x)
    except :
        pass

#The "scrape_row" function scrapes all the content from a row
def scrape_row(row, header_indexes) :

    #The "player_name" string is the name of the player in this row
    player_name = row.find("th").text

    #Return the player name, and a list of each data point that is of interest based on the "header_indexes" list, which is derived from the "tables_to_scrape" dictionary
    return player_name, [convert_to_float_or_none(data_point.text) for data_point_index, data_point in enumerate(row.find_all("td")) if data_point_index in header_indexes]

#The "scrape_headers_row" function returns a list of indexes of data points that are desired from a table
def scrape_headers_row(headers_row, desired_data_points) :

    #Return the list of indexes such that the aria-label of the header for this column is in the "desired_data_points" list
    return [header_index for header_index, header in enumerate(headers_row.find_all("th")[1:]) if header["aria-label"] in desired_data_points]

#The "scrape_table" function scrapes all the content from a table
def scrape_table(table, season) :

    #The "caption" string is the caption of the table
    caption = table.find("caption").text.split(season)[0][:-1]

    goalkeeper = False
    
    if caption in goalkeeper_tables_to_scrape :
        goalkeeper = True
        rows_to_scrape = goalkeeper_tables_to_scrape[caption]
    else :
        #If the caption is not within the relevant tables, return None
        if not caption in tables_to_scrape :
            return None
        rows_to_scrape = tables_to_scrape[caption]

    #The "all_rows" list is the list of row bs4 classes from this table
    all_rows = table.find_all("tr")

    #The "headers_row" class is the second row of the table, which contains all the names of each data point present in this table
    headers_row = all_rows[1]

    #The "header_indexes" list is the list of indexes for each desired data point
    header_indexes = scrape_headers_row(headers_row, rows_to_scrape)

    #Loop through each row in the table (besides the first two rows, which are header rows)
    for row in all_rows[2:] :

        if float(row.find('td', {"data-stat": 'minutes_90s'}).text) >= ninetys_played_minimum :

            #Call the "scrape_row" function to scrape the content of this row
            player_name, row_data = scrape_row(row, header_indexes)

        if goalkeeper :
            if not player_name in goalkeepers :
                goalkeepers[player_name] = row_data
            else :
                goalkeepers[player_name] = goalkeepers[player_name]+row_data

        else :
            if not player_name in goalkeepers :
                if not player_name in players :
                    players[player_name] = row_data
                else :
                    players[player_name] = players[player_name]+row_data
        
def remove_totals(stats) :
    if "Squad Total" in stats :
        del stats["Squad Total"]
    if "Opponent Total" in stats :
        del stats["Opponent Total"]
    
#The "scrape" function scrapes all the content from a team page
def scrape(url) :

    #The "request" object is the html content from the given url
    request = requests.get(url)

    #The "soup" object is the beautiful soup object we will call .find() and .find_all() for certain tags and extract their text
    soup = BeautifulSoup(request.content, "html.parser")

    #The "season" string is the season for these stats found at the header of the page. Example: "2023-24"
    season = soup.find("h1").text.split(" ")[0][1:]

    #Loop through each table in the page
    for table in soup.find_all("table") :

        #Call the "scrape_table" function to scrape the content of this table
        scrape_table(table, season)

    remove_totals(players)
    remove_totals(goalkeepers)

    for key in players :
        print(key, players[key])
    print()

    for key in goalkeepers :
        print(key, goalkeepers[key])


scrape("https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats") 
