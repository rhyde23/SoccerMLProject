#Transfermarkt Scraping script

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#Import unidecode for removing accents from letters in strings
from unidecode import unidecode

#The "scrape_from_transfermakt_page" function scrapes the name, position, and market value of each player present on the page
def scrape_from_transfermakt_page(url) :

    #The "headers" dictionary specifies to the requests.get() function that we're legit.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}

    #The "request" object is the html content from the given url
    request = requests.get(url, headers=headers)

    #The "soup" object is the beautiful soup object that we will find the player's url from 
    soup = BeautifulSoup(request.content, "html.parser")

    #The "tbody" object is the div section of the page's html whose class is "responsive-table", this is the final standings of the league.
    tbody = soup.find("div", {"class": 'responsive-table'})

    #The "transfermarkt_stats" dictionary is the dictionary that will contain all the team's players as the keys and the player's [position, price] as the corresponding value
    transfermarkt_stats = {}

    #Loop through each row in the "responsive-table"
    for row in tbody.find_all("tr")[1:] :

        #Get the player info, which will include name, position, and price by manipulating the td columns's text for this row
        player_info = [td.text.replace("\n", "").replace("\xa0", "").strip() for td in row.find_all("td")][3:]

        #Account for weird cases, make sure "player_info" isn't an empty array
        if player_info != [] :

            #Unpack the name, position, and price
            name, position, price = unidecode(player_info[0]), player_info[1], player_info[-1]

            #Add a value in "transfermarkt_stats" with the player's name as the key and [position, price] as the value
            transfermarkt_stats[name] = [position, price]

    #Return the "transfermarkt_stats" dictionary
    return transfermarkt_stats

