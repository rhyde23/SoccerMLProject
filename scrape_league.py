#Scrape League
import scrape_from_fbref_page, scrape_from_transfermarkt

def scrape_team(fbref_link, transfermarkt_link) :
    fbref_stats, fbref_gk_stats = scrape_from_fbref_page.scrape(fbref_link)
    transfermarkt_stats = scrape_from_transfermarkt.scrape_from_transfermakt_page(transfermarkt_link)
    
    for fbref_key in fbref_stats :
        transfermarkt = transfermarkt_stats[fbref_key]
        print(transfermarkt)

scrape_team("https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats", "https://www.transfermarkt.com/manchester-city/kader/verein/281/saison_id/2023")
