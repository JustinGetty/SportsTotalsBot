import pandas as pd
import datetime


def customStringLimiter(string, maxLength):
    return string[:maxLength]
def createBaseFrame(baseFrame):
    compareFrame = pd.DataFrame()
    for i in baseFrame['Commence Time']:
        j = str(i).replace("T", " ").replace("Z", " ")
        jLimited = customStringLimiter(j, 16) 
        currentTime = str(datetime.datetime.now()) 
        currentTimeLimited = customStringLimiter(currentTime, 16)
        #FIX THIS CODE TO APPEND START TIME ROW TO COMPARE FRAME
        #compareFrame.append(baseFrame.loc(i))

if __name__ == '__main__':
    data1 = {
        'Event ID': ['a58faa4e75b965d50446c73bbeef1d82', '39fe52ee8c209de2fc87fc0f692e6094'],
        'Home Team': ['Detroit Pistons', 'Cleveland Cavaliers'],
        'Away Team': ['Charlotte Hornets', 'Phoenix Suns'],
        'Commence Time': ['2023-12-16T23:00:00Z', '2023-12-16T21:00:00Z'],
        'Totals': [217.0, 220.5]
    }


    df1 = pd.DataFrame(data1)

    createBaseFrame(df1)

