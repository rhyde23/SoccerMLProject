#Scraping script

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#The "tables_to_scrape" list contains all of the relevant tables for data scraping
tables_to_scrape = [
    "Standard Stats",
    "Scores & Fixtures",
    "Goalkeeping",
    "Advanced Goalkeeping",
    "Shooting",
    "Passing",
    "Pass Types",
    "Goal and Shot Creation",
    "Defensive Actions",
    "Possession",
    "Playing Time",
    "Miscellaneous Stats"
]

#The "scrape_row" function scrapes all the content from a row
def scrape_row(row) :

    #The "player_name" string is the name of the player in this row
    player_name = row.find("th").text
    
    print(player_name)

#The "scrape_table" function scrapes all the content from a table
def scrape_table(table, season) :

    #The "caption" string is the caption of the table
    caption = table.find("caption").text.split(season)[0][:-1]

    #If the caption is not within the relevant tables, return None
    if not caption in tables_to_scrape :
        return None
    
    print(caption)

    #Loop through each row in the table 
    for row in table.find_all("tr") :

        #Call the "scrape_row" function to scrape the content of this row
        scrape_row(row)
        
    quit()
    
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
