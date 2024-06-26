#Scrape League
import scrape_from_fbref_page, scrape_from_transfermarkt

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}

def scrape_team(fbref_team_link, transfermarkt_team_link) :
    fbref_stats, fbref_gk_stats = scrape_from_fbref_page.scrape(fbref_team_link)
    transfermarkt_stats = scrape_from_transfermarkt.scrape_from_transfermakt_page(transfermarkt_team_link)
    
    for fbref_key in fbref_stats :
        transfermarkt = transfermarkt_stats[fbref_key]
        print(transfermarkt)


def get_fbref_team_links(fbref_link) :
    
    request = requests.get(fbref_link, headers=headers)

    #The "soup" object is the beautiful soup object that we will find the player's url from 
    soup = BeautifulSoup(request.content, "html.parser")

    return [td.find("a")["href"] for td in soup.find_all("td", {"data-stat": "team"})[:20]]

def get_transfermarkt_team_links(transfermarkt_link) :
    
    request = requests.get(transfermarkt_link, headers=headers)

    #The "soup" object is the beautiful soup object that we will find the player's url from 
    soup = BeautifulSoup(request.content, "html.parser")

    links = []
    for a in soup.find("div", {"class":"box tab-print"}).find_all("a") :
        link = a["href"]
        if link != "#" and not link in links :
            links.append(link)
    return links[:-1]

def scrape_league(fbref_link, transfermarkt_link) :
    for matching_link in zip(get_fbref_team_links(fbref_link), get_transfermarkt_team_links(transfermarkt_link)) :
        print(matching_link)
    

scrape_league("https://fbref.com/en/comps/10/Championship-Stats", "https://www.transfermarkt.com/championship/startseite/wettbewerb/GB2")
#scrape_team("https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats", "https://www.transfermarkt.com/manchester-city/kader/verein/281/saison_id/2023")

#https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats
