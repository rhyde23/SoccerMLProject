#Scrape League
import scrape_from_fbref_page, scrape_from_transfermarkt

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#The "headers" dictionary specifies to the requests.get() function that we're legit.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}

#The "scrape_team" function combines the data from FBRef and Transfermarkt and records it in the SQl database
def scrape_team(fbref_team_link, transfermarkt_team_link) :

    #Unpack the player stats and the goalkeeper stats from calling "scrape_from_fbref_page.scrape" 
    fbref_stats, fbref_gk_stats = scrape_from_fbref_page.scrape(fbref_team_link)

    #Call the "scrape_from_transfermarkt.scrape_from_transfermakt_page()" function to get the positions and prices for all the players on the team
    transfermarkt_stats = scrape_from_transfermarkt.scrape_from_transfermakt_page(transfermarkt_team_link)

    #Iterate through each key from the "fbref_stats" (player name)
    for fbref_key in fbref_stats :

        #Get the corresponding transfermarkt stats for this player name
        transfermarkt = transfermarkt_stats[fbref_key]

        print(transfermarkt)

#The "get_fbref_team_links" function gets all the links to team pages from an FBRef league page.
def get_fbref_team_links(fbref_link) :

    #The "request" object is the html content from the given fbref link 
    request = requests.get(fbref_link, headers=headers)

    #The "soup" object is the beautiful soup object that we will find the player's url from 
    soup = BeautifulSoup(request.content, "html.parser")

    #Return the list of links from td columns if the "data-stat" tag for the td is "team"
    return [td.find("a")["href"] for td in soup.find_all("td", {"data-stat": "team"})[:20]]

#The "get_transfermarkt_team_links" function gets all the links to team pages from a Transfermarkt league page
def get_transfermarkt_team_links(transfermarkt_link) :

    #The "request" object is the html content from the given transfermarkt link 
    request = requests.get(transfermarkt_link, headers=headers)

    #The "soup" object is the beautiful soup object that we will find the player's url from 
    soup = BeautifulSoup(request.content, "html.parser")

    #The "links" list will be filled with links from the page
    links = []

    #Iterate through each link in the "box tab-print" div (League table div table)
    for a in soup.find("div", {"class":"box tab-print"}).find_all("a") :

        #Get the href link from this object
        link = a["href"]

        #Filter out weird instances and make sure the link isn't already in the list (some repeats)
        if link != "#" and not link in links :

            #Add the link to the list
            links.append(link)

    #Return the "links" list with the last item stripped off because it a link to another part of the league page.
    return links[:-1]

#The "scrape_league" function is the main function for this script, will iterate through each matching of fbref team link and transfermarkt team link and call "scrape_team"
def scrape_league(fbref_league_link, transfermarkt_league_link) :
    for matching_link in zip(get_fbref_team_links(fbref_league_link), get_transfermarkt_team_links(transfermarkt_league_link)) :
        print(matching_link)
    

scrape_league("https://fbref.com/en/comps/10/Championship-Stats", "https://www.transfermarkt.com/championship/startseite/wettbewerb/GB2")
#scrape_team("https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats", "https://www.transfermarkt.com/manchester-city/kader/verein/281/saison_id/2023")

#https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats
