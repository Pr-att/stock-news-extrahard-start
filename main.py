import requests
from datetime import datetime, timedelta
from twilio.rest import Client

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': '{Your Alphavantage api key here}',
}
r = requests.get('https://www.alphavantage.co/query', params=parameters)
data = r.json()
r = data['Time Series (Daily)']
today = datetime.now()
n_days_ago = today - timedelta(days=2)
n0_days_ago = today - timedelta(days=3)
diff = float(r[f'{n_days_ago.date()}']['4. close']) - \
       float(r[f'{n0_days_ago.date()}']['4. close'])
ans = (diff / float(r[f'{n0_days_ago.date()}']['4. close'])) * 100
percent = round(ans, 2)

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

params = {
    'q': STOCK,
    'from': f'{today - timedelta(days=1)}',
    'sortBy': 'publishedAt',
    'apikey': '{your news_api_key here}'
}
if percent > 0:
    response = requests.get('https://newsapi.org/v2/everything', params=params)
    title = response.json()['articles'][0]['title']
    description = response.json()['articles'][0]['description']
    high = f"TSLA: 🔺{percent}%\nHeadline: {title}.\n\nBrief: {description}"
    account_sid = '{Your account_sid here}'
    auth_token = '{Your auth_token here}'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=high,
        from_='+15599345136',
        to='{Your phone number here}'
    )
    print(message.sid)

elif percent < 0:
    response = requests.get('https://newsapi.org/v2/everything', params=params)
    title = response.json()['articles'][0]['title']
    description = response.json()['articles'][0]['description']
    low = f"TSLA: 🔻{percent}%\nHeadline: {title}.\n\nBrief: {description}"
    account_sid = '{Your account_sid here}'
    auth_token = '{Your auth_token here}'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=low,
        from_='+15599345136',
        to='{Your phone number here}'
    )
    print(message.sid)

# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
