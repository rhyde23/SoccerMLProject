#Populate Database

import scrape_league

league_link_pairs = {
    "Premier League":("https://fbref.com/en/comps/9/Premier-League-Stats", "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1"),
    "Ligue One":("https://fbref.com/en/comps/13/Ligue-1-Stats", "https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1"),
    "Serie A":("https://fbref.com/en/comps/11/Serie-A-Stats", "https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1"),
    "Bundesliga":("https://fbref.com/en/comps/20/Bundesliga-Stats", "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1"),
    "La Liga":("https://fbref.com/en/comps/12/La-Liga-Stats", "https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1"),
}

def populate() :
    for league_name in league_link_pairs :
        fbref_league_link, transfermarkt_league_link = league_link_pairs[league_name]
        scrape_league.scrape_league(fbref_league_link, transfermarkt_league_link, "2023-2024", league_name)



populate()
