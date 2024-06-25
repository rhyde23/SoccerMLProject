#Transfermarkt Scraping script

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#The "get_transfermarkt_player_url" function scrapes the url of the top search result for a player name query
def get_transfermarkt_player_url(player_name) :

    #The "query_link" string formats the search for the player's url by using the "player_name" string and replacing spaces with plus signs
    query_link = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query="+player_name.replace(" ", "+")

    #The "request" object is the html content from the given query link

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
    request = requests.get(query_link, headers=headers)

    #The "soup" object is the beautiful soup object that we will find the player's url from 
    soup = BeautifulSoup(request.content, "html.parser")

    #print(soup)
    
    for row in soup.find_all("tr")) :
        print(row)
    return "https://www.transfermarkt.com"+soup.find("tr").find("a")["href"]

#The "scrape_from_transfermakt" function scrapes position and Market Value from Transfermarkt
def scrape_from_transfermakt(url) :

    #The "request" object is the html content from the given url
    request = requests.get(url)

    #The "soup" object is the beautiful soup object we will call .find() and .find_all() for certain tags and extract their text
    soup = BeautifulSoup(request.content, "html.parser")

print(get_transfermarkt_player_url("Mateo Kovačić"))
