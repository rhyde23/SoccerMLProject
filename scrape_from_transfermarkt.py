#Transfermarkt Scraping script

#Import requests library for requests for html content of websites 
import requests

#Import beautiful soup library for parsing html content
from bs4 import BeautifulSoup

#Import unidecode for removing accents from letters in strings
from unidecode import unidecode

#The "convert_market_value_to_int" function converts the market value strings from Transfermarkt to integers
def convert_market_value_to_int(mv_string) :
    
    #The "m_or_k" string is the last character of the market value string, either 'm' or 'k' for million or thousand
    m_or_k = mv_string[-1]

    #Cut off the first and last characters of "mv_string". (The Euro currency character and the m or k)
    mv_string = mv_string[1:][:-1]

    #If "m_or_k" is 'm'
    if m_or_k == "m" :

        #Split the mv_string by the .
        first_half, second_half = mv_string.split(".")

        #Return the integer version
        return (int(first_half)*1000000)+(int(second_half)*10000)

    #If "m_or_k" is 'k'
    elif m_or_k == "k" :

        #Return the integer version
        return int(mv_string)*1000

    #If "m_or_k" is neither 'm' or 'k'
    else :
        
        #Return None
        return None
    
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

            #Unpack the name, position, and price (converted to integer)
            name, position, price = unidecode(player_info[0]), player_info[1], convert_market_value_to_int(player_info[-1])

            #If the price is not None
            if price != None :

                #Add a value in "transfermarkt_stats" with the player's name as the key and [position, price] as the value
                transfermarkt_stats[name] = [position, price]

    #Return the "transfermarkt_stats" dictionary
    return transfermarkt_stats
