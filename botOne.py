import requests
import os
import pandas as pd
API_KEY = 'b23fc22e2b337a48421b2b94b1fa5e80'

SPORT = 'basketball_nba' # NBA sport key
REGIONS = 'us' # Focusing on US region
MARKETS = 'totals' #Totals market
ODDS_FORMAT = 'decimal' # Using decimal format for odds
DATE_FORMAT = 'iso' # Using ISO format for dates

# Fetching in-season sports (optional step, but useful for confirmation)
sports_response = requests.get(
    'https://api.the-odds-api.com/v4/sports',
    params={'api_key': API_KEY}
)


odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code == 200:
    odds_json = odds_response.json()
#    print('Number of NBA events:', len(odds_json))
#    print(odds_json) # This prints the fetched odds data
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])
else:
    print(f'Its broken')


odds_data = odds_json

events = []
eventIdCleaner = []
for event in odds_data:
    event_id = event['id']
    sport_key = event['sport_key']
    sport_title = event['sport_title']
    commence_time = event['commence_time']
    home_team = event['home_team']
    away_team = event['away_team']

    for bookmaker in event['bookmakers']:
        bookmaker_key = bookmaker['key']
        bookmaker_title = bookmaker['title']

        for market in bookmaker['markets']:
            if market['key'] == 'totals':
                for outcome in market['outcomes']:
                    team = outcome['name']
                    price = outcome['price']
                    point = outcome['point']
                    if event_id not in eventIdCleaner:
                        events.append([event_id, home_team, away_team, 
                                    bookmaker_title, point])
                        
                    eventIdCleaner.append(event_id)
columns = ['Event ID', 'Home Team', 'Away Team', 
           'Bookmaker Title', 'Totals']
df = pd.DataFrame(events, columns=columns)

print(df)
