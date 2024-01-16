import requests
import os
from twilio.rest import Client
#from twilio.http.http_client import TwilioHttpClient 
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


account_sid = "YOUR ACCOUNT SID"


STOCK_API_KEY = "YOUR API KEY"
NEWS_API_KEY = "YOUR NEWS API KEY"
TWILIO_API_KEYS = "YOUR TWILIO API KEY"
stock_parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT,params=stock_parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in stock_data.items()]
yesterday_closing_price = data_list[0]["4. close"]
day_before_yesterday_closing_price = data_list[1]["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


difference_percentage = round((difference / float(yesterday_closing_price)) * 100)


if abs(difference_percentage) > 5:


    
    news_parameters = {
        'q':COMPANY_NAME,
        #'from':'2023-11-30',
        #'sortBy':"publishedAt",
        'apiKey':NEWS_API_KEY,
        
    }
     
    news_response = requests.get(url=NEWS_ENDPOINT,params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]  
    three_articles = articles[:4]
    formatted_articles = [f" {STOCK_NAME}: {up_down}{difference_percentage}%.\nHeadlines:{article['title']}. \nBrief: {article['description']}" for article in three_articles]
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https':os.environ['https_proxy']}
    client = Client(account_sid,TWILIO_API_KEYS)
    for article in formatted_articles:
        message = client.messages.create(
            body={article},
            from_="YOUR TWILIO NUMBER",
            to="YOUR VERIFIED NUMBER"
        )
        print(message.status)