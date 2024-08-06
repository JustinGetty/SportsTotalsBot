Usage:

The user will have to enter their email and password, as well as the email they desire the notification to be sent to (it can be the same if you would like to alert yourself). You will need to enter your own api key from https://the-odds-api.com/#get-access, which has free tier that permits 500 requests per month. You will need Pandas installed, and the program will constantly run so it needs to be ran on a server or a machine that will not be turned off.

How it works:

At the game start time, an api request will be sent to the odds service and the data comes back in JSON. JSON is not very pleasant to work with in Python, so I immediately convert it to a dataframe. This frame will be created with the odds for the game at the start. After that, every 20 minutes it will check the current total against that original total via new api requests. If the difference is 15 or more in either direction, an alert will be sent via ssl. Once an alert is sent, that unique game id is added to a new frame, and from then on every time it detects a change in the difference it will check if an alert was already sent. This will avoid duplicate alerts and spam. The reason 20 minutes was chosen and not checking every minute is that NBA games typically operate in a 5 hour window 6 days a week. Checking every 20 minutes for 5 hours 6 days a week adds to a little over 400 requests per month when you calculate in initial frames and if there are games that run late. This keeps the api request usage under 500, which is the limit for the free tier. 

Code extensibilty:

I built this in a way that if you wanted additonal game information, such as other odds or other games, it would be simple to pull these odds into their own frame. By nature of the api request, more data is pulled then needed, this way if a user wanted to also be alerted of a change in say moneyline odds, it would not use any extra requests.

Example alert:

![image](https://github.com/JustinGetty/SportsTotalsBot/assets/163033045/ff999db3-f2d5-480b-9099-99323e89c1f8)



