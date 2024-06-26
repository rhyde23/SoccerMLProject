#Transfermarkt Scraping script

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#Import unidecode for removing accents from letters in strings
from unidecode import unidecode

#The "scrape_from_transfermakt_page" function scrapes the name, position, and market value of each player present on the page
def scrape_from_transfermakt_page(url) :

    #The "request" object is the html content from the given query link
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}

    request = requests.get(url, headers=headers)

    #The "soup" object is the beautiful soup object that we will find the player's url from 
    soup = BeautifulSoup(request.content, "html.parser")

    tbody = soup.find("div", {"class": 'responsive-table'})

    transfermarkt_stats = {}
    
    for row in tbody.find_all("tr")[1:] :
        player_info = [td.text.replace("\n", "").replace("\xa0", "").strip() for td in row.find_all("td")][3:]
        if player_info != [] :
            name, position, price = unidecode(player_info[0]), player_info[1], player_info[-1]
            transfermarkt_stats[name] = [position, price]

    return transfermarkt_stats

#scrape_from_transfermakt_page("https://www.transfermarkt.com/manchester-city/kader/verein/281/saison_id/2023"))

