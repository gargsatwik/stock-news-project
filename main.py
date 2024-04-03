import requests
import datetime
import smtplib
import random
import os

STOCK = os.environ.get('STOCK')
COMPANY_NAME = os.environ.get('COMPANY_NAME')
STOCK_API_KEY = os.environ.get('STOCK_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
TODAY = datetime.datetime.now().date()
MY_EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('MY_PASSWORD')

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

news_parameters = {
    "country": "us",
    "apiKey": NEWS_API_KEY,
}

stock_response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
stock_data = stock_response.json()
day1_close = float(stock_data["Time Series (Daily)"][str(TODAY - datetime.timedelta(days=1))]["4. close"])
day2_close = float(stock_data["Time Series (Daily)"][str(TODAY - datetime.timedelta(days=2))]["4. close"])

news_response = requests.get(url="https://newsapi.org/v2/top-headlines", params=news_parameters)
news_data = news_response.json()
top_news = []
for i in range(2):
    article = {
        "title": news_data["articles"][i]['title'],
        "description": news_data["articles"][i]['description']
    }
    top_news.append(article)

change = round(((day1_close - day2_close)/day1_close)*100, 2)

news_to_be_sent = random.choice(top_news)

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL,
                        to_addrs=os.environ.get('TO_ADDRESS'),
                        msg=f"Subject:Stock Update\n\n{STOCK}: {change}%\nHeadline: {news_to_be_sent['title']}\nBrief:"
                            f" {news_to_be_sent['description']}")
    
