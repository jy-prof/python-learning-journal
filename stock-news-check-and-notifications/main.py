import os
import requests
from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient
from dotenv import load_dotenv; load_dotenv()


# you can choose another one
STOCK_NAME = "MSFT"
COMPANY_NAME = "Microsoft Corp"

percentage_threshold = 0.5    # you can set it to 5 or 1 or ... For testing purpose I put 0.5

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")
MY_OWN_NUMBER = os.getenv("MY_OWN_NUMBER")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")



stock_params = {
    "apikey": STOCK_API_KEY,
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
}

# Get yesterday's closing stock price.
# perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
# https://www.alphavantage.co/query?apikey=[PASTE YOUR API KEY HERE ]&function=TIME_SERIES_DAILY&symbol=MSFT to test it
response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print(yesterday_closing_price)

# https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by X% (percentage_threshold)
# between yesterday and the day before yesterday, then print("Get News").

# Get the day before yesterday's closing stock price
day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday["4. close"])
print(day_before_yesterday_closing_price)

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
difference = yesterday_closing_price - day_before_yesterday_closing_price

up_down = None   # to setup the icon in the message to send
if difference > 0:
    up_down = "▲"
elif difference < 0:
    up_down = "🔻"
else:
    up_down = "➖"
# print(difference) # to test it


# Percentage Increase = (V2 − V1) / V1 * 100
diff_percent = round(difference / day_before_yesterday_closing_price * 100)
# print(f"{diff_percent}%")   # to test/check it

news_params = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,
    # "from": yesterday_data,
    "sortBy": "popularity",
}


# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
# https://www.w3schools.com/python/ref_func_abs.asp

# percentage_threshold = 0.5  to test it first, then you can setup the percentage_threshold = to 5 or another number
if abs(diff_percent) > percentage_threshold:

    # https://newsapi.org/    Instead of printing ("Get News"),
    # actually get the first 3 news pieces for the COMPANY_NAME.
    # and use the News API to get articles related to the COMPANY_NAME.

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)

    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    # print(articles) # list of dictionaries
    # print(f"{articles[0]}\n{articles[1]}\n{articles[2]}\n")


    # Use Python slice operator to create a list that contains the first 3 articles.
    # https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    # print(three_articles)

    # Use https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
    # to try and send a separate WhatsApp message with each article's title and description to your phone number.

    # create a new list of the first 3 articles headline and description using list comprehension.
    formatted_articles = [
        (f'{STOCK_NAME} moved {up_down}{diff_percent}%\nHeadline: {article["title"]}.\n'
         f'Brief: {article["description"]}\n\n— Your daily stock buzz 📊')
        for article in three_articles
    ]

    # Send each article as a separate message via Twilio.
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            # to use WhatsApp with Twilio, you must first activate the WhatsApp sandbox in your Twilio console
            from_=f"whatsapp:{WHATSAPP_NUMBER}",
            # now put your OWN phone number (in .env file) for whatsapp messages
            to=f"whatsapp:{MY_OWN_NUMBER}",
        )




