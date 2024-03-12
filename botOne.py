import requests
import os
import pandas as pd
import datetime
import time
import smtplib
import ssl
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "justingetty55@gmail.com"
RECEIVER_EMAIL = "matthewgeib1365@gmail.com"
EMAIL_PASSWORD = "fbdf fkib pgcw jgak"

API_KEY = 'b23fc22e2b337a48421b2b94b1fa5e80'

def getTotals():
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
    return odds_json
#Find more implicit compare method
def compareOutputs(df1, df2):
    # Merge the two DataFrames on 'Event ID'
    merged_df = pd.merge(df1, df2, on='Event ID', suffixes=('_df1', '_df2'))

    # Calculate the absolute difference in 'Totals' and add it as a new column
    merged_df['Totals Difference'] = (merged_df['Totals_df1'] - merged_df['Totals_df2']).abs()

    # Filter rows where the difference in 'Totals' is 15 or more
    significant_diffs = merged_df[merged_df['Totals Difference'] >= 15]

    # Check if there are any significant differences
    if significant_diffs.empty:
        print("No significant differences in Totals found.")
        return False, None  # Return False indicating no significant differences, and None for the DataFrame
    else:
        # If significant differences were found, print them and return True and the DataFrame
        print(significant_diffs[['Event ID', 'Totals_df1', 'Totals_df2', 'Totals Difference']])
        return True, significant_diffs[['Event ID', 'Totals_df1', 'Totals_df2', 'Totals Difference']]

def cleanShittyJson():
    odds_data = getTotals()
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
    return df

def sendEmail(message):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)

#FIX to pull data at start of the game and then compare every 20 minutes to the start 
if __name__ == '__main__':
    while True:
        while datetime.datetime.now().hour >= 18 and datetime.datetime.now().hour < 24: 
            print("Prompting 1")
            data = cleanShittyJson()
            print(data)
            time.sleep(1200) 
            print("Prompting 2")
            dataTwo = cleanShittyJson()
            print(dataTwo)

            hasDifference, difference = compareOutputs(data, dataTwo)
            if hasDifference:
                print(difference)
                message = f"From: {SENDER_EMAIL}\nTo: {RECEIVER_EMAIL}\nSubject: Change in totals\n\nHere is the difference: \n {difference}"
                sendEmail(message)
                print("email sent")
            else:
                print("No significant diference, no email sent")




