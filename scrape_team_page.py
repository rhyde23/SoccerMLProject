#Scraping script

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#The "tables_to_scrape" dictionary contains all of the relevant tables for data scraping and which stats from those tables are of interest
tables_to_scrape = {
    "Goalkeeping":[],
    "Advanced Goalkeeping":[],
    "Shooting":[],
    "Passing":['Passes Completed', 'Passes Attempted (Short)', 'Pass Completion % (Short)', 'Passes Completed (Medium)', 'Pass Completion % (Medium)', 'Passes Completed (Long)'],
    "Pass Types":[],
    "Goal and Shot Creation":[],
    "Defensive Actions":[],
    "Possession":[],
    "Playing Time":[],
    "Miscellaneous Stats":[],
}

#The "get_all_aria_labels" function simply returns a list of all the stats present in a data table (for development purposes)
def get_all_aria_labels(headers_row) :

    #Return a list of each aria-label for each header in the row of headers
    return [header["aria-label"] for header in headers_row.find_all("th")]

#The "scrape_row" function scrapes all the content from a row
def scrape_row(row, header_indexes) :

    #The "player_name" string is the name of the player in this row
    player_name = row.find("th").text

    #Return the player name, and a list of each data point that is of interest based on the "header_indexes" list, which is derived from the "tables_to_scrape" dictionary
    return player_name, [data_point.text for data_point_index, data_point in enumerate(row.find_all("td")) if data_point_index in header_indexes]

#The "scrape_headers_row" function returns a list of indexes of data points that are desired from a table
def scrape_headers_row(headers_row, desired_data_points) :

    #Return the list of indexes such that the aria-label of the header for this column is in the "desired_data_points" list
    return [header_index for header_index, header in enumerate(headers_row.find_all("th")[1:]) if header["aria-label"] in desired_data_points]

#The "scrape_table" function scrapes all the content from a table
def scrape_table(table, season) :

    #The "caption" string is the caption of the table
    caption = table.find("caption").text.split(season)[0][:-1]

    #If the caption is not within the relevant tables, return None
    if not caption in tables_to_scrape :
        return None
    
    print(caption)

    #The "all_rows" list is the list of row bs4 classes from this table
    all_rows = table.find_all("tr")

    #The "headers_row" class is the second row of the table, which contains all the names of each data point present in this table
    headers_row = all_rows[1]

    #The "header_indexes" list is the list of indexes for each desired data point
    header_indexes = scrape_headers_row(headers_row, tables_to_scrape[caption])

    print(tables_to_scrape[caption])

    #Loop through each row in the table (besides the first two rows, which are header rows)
    for row in all_rows[2:] :
        
        #Call the "scrape_row" function to scrape the content of this row
        print(scrape_row(row, header_indexes))
        
    
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


scrape("https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats") 
