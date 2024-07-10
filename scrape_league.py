#Scrape League
import scrape_from_fbref_page, scrape_from_transfermarkt, database_management

#Import time library for the .sleep() function to avoid 429 request error
import time

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#The "headers" dictionary specifies to the requests.get() function that we're legit.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}

#The "scrape_team" function combines the data from FBRef and Transfermarkt and records it in the SQl database
def scrape_team(fbref_team_link, transfermarkt_team_link, database_league_name) :

    #Unpack the player stats and the goalkeeper stats from calling "scrape_from_fbref_page.scrape" 
    fbref_stats, fbref_gk_stats = scrape_from_fbref_page.scrape(fbref_team_link)

    #Call the "scrape_from_transfermarkt.scrape_from_transfermakt_page()" function to get the positions and prices for all the players on the team
    transfermarkt_stats = scrape_from_transfermarkt.scrape_from_transfermakt_page(transfermarkt_team_link)

    #Iterate through each key from the "fbref_stats" (player name)
    for fbref_key in fbref_stats :

        #If the player's name is in the "transfermarkt_stats" dictionary
        if fbref_key in transfermarkt_stats :

            #Get the corresponding transfermarkt stats for this player name
            transfermarkt = transfermarkt_stats[fbref_key]

            #Call the "enter_player_in_database" to enter this player in the league table in the SQL database
            database_management.enter_player_in_database(database_league_name, fbref_key, transfermarkt[0], transfermarkt[1], fbref_stats[fbref_key])

    #Iterate through each key from the "fbref_gk_stats" (player name)
    for fbref_gk_key in fbref_gk_stats :

        #If the GK player's name is in the "transfermarkt_stats" dictionary
        if fbref_gk_key in transfermarkt_stats :

            #Get the corresponding transfermarkt stats for this GK player name
            transfermarkt = transfermarkt_stats[fbref_gk_key]

            #Call the "enter_player_in_database" to enter this GK player in the GK league table in the SQL database
            database_management.enter_player_in_database(database_league_name+"_GK", fbref_gk_key, transfermarkt[0], transfermarkt[1], fbref_gk_stats[fbref_gk_key])

#The "get_fbref_team_links" function gets all the links to team pages from an FBRef league page.
def get_fbref_team_links(fbref_link) :

    #The "request" object is the html content from the given fbref link 
    request = requests.get(fbref_link, headers=headers)

    #The "soup" object is the beautiful soup object that we will find the player's url from 
    soup = BeautifulSoup(request.content, "html.parser")

    #Return the list of links from td columns if the "data-stat" tag for the td is "team"
    return [td.find("a")["href"] for td in soup.find_all("td", {"data-stat": "team"})[:20]]

#The "get_transfermarkt_team_links" function gets all the links to team pages from a Transfermarkt league page
def get_transfermarkt_team_links(transfermarkt_link, season_year) :

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
        if link != "#" :

            #The "link_slash_splitted" list is the link splitted by forward slash
            link_slash_splitted = link.split("/")

            #Build the actual Transfermarkt link for this season 
            link = "/".join(link_slash_splitted[:-5]+["kader", "verein", link_slash_splitted[-3], "plus", "0", "galerie", "0?saison_id="+season_year.split("-")[0]])

            #If the link is not already in "links"
            if not link in links :

                #Add the link to "links"
                links.append(link)

    #Return the "links" list with the last item stripped off because it a link to another part of the league page.
    return links[:-1]

#The "scrape_league" function is the main function for this script, will iterate through each matching of fbref team link and transfermarkt team link and call "scrape_team"
def scrape_league(fbref_league_link, transfermarkt_league_link, season_year, official_league_name) :

    #Open the connection to the SQL Database by calling the "open_connection" function
    database_management.open_connection()
    
    #The "database_league_name" is the official league name except underscores replace spaces
    database_league_name = official_league_name.replace(" ", "_")

    #If this database league name does not exist in the SQL Database
    if not database_management.table_exists(database_league_name) :

        #Create the table with this name
        database_management.create_tables(database_league_name)

    #Split the Fbref League link by forward slash
    splitted_by_slashes = fbref_league_link.split("/")

    #Build the new link based on the "season_year" string
    fbref_league_link = "/".join(splitted_by_slashes[:-1]+[season_year, season_year+"-"+splitted_by_slashes[-1]])

    #Iterate through each match of Fbref team link and Transfermarkt team link
    for matching_link in zip(get_fbref_team_links(fbref_league_link), get_transfermarkt_team_links(transfermarkt_league_link+"/?saison_id="+season_year.split("-")[0], season_year)) :
        
        #Call the "scrape_team" function with this matching team link pair
        scrape_team("https://fbref.com"+matching_link[0], "https://www.transfermarkt.com"+matching_link[1], database_league_name)

        #Wait 5 seconds to avoid the 429 Request Timeout Error from FBRef
        time.sleep(5)

    #Close the connection to the SQL Database by calling the "close_connection" function
    database_management.close_connection()
