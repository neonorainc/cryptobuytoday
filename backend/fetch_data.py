import requests
import json
from datetime import datetime
import pandas as pd
import talib

# ---------- PARAMETERS ----------
COINGECKO_API = "https://api.coingecko.com/api/v3/coins/markets"
NEWS_API = "https://newsapi.org/v2/everything"
NEWS_KEY = "1423ed75dc854279a21166e5a06f1592"  # Replace with your key
VS_CURRENCY = "usd"
TOP_N_COINS = 20

# ---------- FETCH MARKET DATA ----------
params = {
    "vs_currency": VS_CURRENCY,
    "order": "market_cap_desc",
    "per_page": TOP_N_COINS,
    "page": 1,
    "sparkline": "true"
}

coins = requests.get(COINGECKO_API, params=params).json()

# ---------- CALCULATE TECHNICAL INDICATORS ----------
top_coins = []
for coin in coins:
    prices = coin.get("sparkline_in_7d", {}).get("price", [])
    if len(prices) < 20:
        continue

    df = pd.DataFrame(prices, columns=["close"])
    close = df['close']

    # RSI (14)
    rsi = talib.RSI(close, timeperiod=14)[-1]

    # MACD
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_last = macd[-1] - macdsignal[-1]

    # SMA (50)
    sma50 = talib.SMA(close, timeperiod=50)[-1]

    # Simple score: RSI + MACD + SMA
    score = 0
    if rsi < 30:  # Oversold
        score += 30
    elif rsi > 70:  # Overbought
        score -= 10

    if macd_last > 0:
        score += 30
    else:
        score -= 10

    if close.iloc[-1] > sma50:
        score += 20
    else:
        score -= 10

    top_coins.append({
        "name": coin['name'],
        "symbol": coin['symbol'].upper(),
        "score": score
    })

# ---------- SENTIMENT ANALYSIS ----------
def fetch_sentiment(coin_name):
    try:
        params = {
            "q": coin_name,
            "apiKey": NEWS_KEY,
            "pageSize": 5,
            "language": "en",
            "sortBy": "publishedAt"
        }
        resp = requests.get(NEWS_API, params=params).json()
        score = 0
        for article in resp.get("articles", []):
            title = article['title'].lower()
            if "bull" in title or "pump" in title:
                score += 5
            elif "bear" in title or "dump" in title:
                score -= 5
        return score
    except:
        return 0

for coin in top_coins:
    sentiment = fetch_sentiment(coin['name'])
    coin['score'] += sentiment

# ---------- SELECT TOP 5 ----------
top5 = sorted(top_coins, key=lambda x: x['score'], reverse=True)[:5]

# ---------- SAVE TO JSON ----------
output = {
    "last_updated": datetime.utcnow().isoformat() + "Z",
    "top5": top5
}

with open("update.json", "w") as f:
    json.dump(output, f, indent=4)
