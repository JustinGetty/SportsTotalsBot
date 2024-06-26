import requests
import os
import pandas as pd
import datetime
import time
import smtplib
import ssl
# Currently checks every 20 minutes for a 15 or more change in the total, sending an email if met
# TODO fix the dataframe for output to include game and time
# TODO adjust logic to pull frame 1 at start of game and reset frame 2 every 20 min to compare
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "EnterYourEmail@gmail.com"
RECEIVER_EMAIL = "EnterRecieverEmail@gmail.com"
#NOTE sometimes google requires an app password when using in inline code, go to your google account and create one
EMAIL_PASSWORD = "EmailPassword"
#API key for odds api
API_KEY = 'api_key'

def getTotals():
    SPORT = 'basketball_nba' # NBA sport key
    REGIONS = 'us' 
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

#TODO Find more implicit compare method
def compareOutputs(df1, df2):
    merged_df = pd.merge(df1, df2, on='Event ID', suffixes=('_df1', '_df2'))

    # Calculate the absolute difference in 'Totals' and add it as a new column
    merged_df['Totals Difference'] = (merged_df['Totals_df1'] - merged_df['Totals_df2']).abs()

    # Filter rows where the difference in 'Totals' is 15 or more
    significant_diffs = merged_df[merged_df['Totals Difference'] >= 15]

    # Select columns to include the team names along with the Event ID and Totals Difference
    # If broke, put event id back in this 'Event ID'
    output_columns = ['Home Team_df1', 'Away Team_df1', 'Totals_df1', 'Totals_df2', 'Totals Difference']

    # Check if there are any significant differences
    if significant_diffs.empty:
        return False, None  # Return False indicating no significant differences, and None for the DataFrame
    else:
        # If significant differences were found, print them and return True and the DataFrame
        return True, significant_diffs[output_columns]



#def baseFrame(baseFrame):
#    compareFrame = pd.DataFrame() 
#    for i in baseFrame['Start Time']:
#        if datetime.datetime.now() == i: 
#            compareFrame.append(baseFrame.loc[i]
            
            

def cleanJson():
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
                                        commence_time, point])
                            
                        eventIdCleaner.append(event_id)
    columns = ['Event ID', 'Home Team', 'Away Team', 
               'Start Time', 'Totals']
    df = pd.DataFrame(events, columns=columns)
    return df

def sendEmail(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)

if __name__ == '__main__':
    print("Bot is active.")
    while True:
        if datetime.datetime.now().hour == 18: 
            homeArray = []
            print("Initial Prompt")
            data = cleanJson()
            while datetime.datetime.now().hour >= 18 and datetime.datetime.now().hour < 24: 
                print("Data Initial")
                print(data)
                time.sleep(1440) 
                print("Prompting 2")
                dataTwo = cleanJson()
                print(dataTwo)

                hasDifference, difference = compareOutputs(data, dataTwo)
                if hasDifference:
                    print(difference)
                    try:
                        homeTeam = str(difference['Home Team_df1'])  
                        if homeTeam in homeArray:
                            print("Difference already reported")
                        else:
                            homeArray.append(homeTeam)
                            message = f"From: {SENDER_EMAIL}\nTo: {RECEIVER_EMAIL}\nSubject: Change in totals\n\nHere is the difference: \n {difference}"
                            sendEmail(message)
                            print("email sent")
                    except:
                        print("Error is in main statement, dont do implicit comparison anymore")
                else:
                    print("No significant diference, no email sent")




