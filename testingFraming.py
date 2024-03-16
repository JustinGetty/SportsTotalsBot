import pandas as pd
import datetime


def customStringLimiter(

def createBaseFrame(baseFrame):
    maxLength = 16

    compareFrame = pd.DataFrame()
    for i in baseFrame['Commence Time']:
        j = str(i).replace("T", " ").replace("Z", " ")
        jLimited = 
        print(j)
        print(datetime.datetime.now())
        #print(datetime.datetime.now().strftime('%M:%S.%f')[:-4])

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

