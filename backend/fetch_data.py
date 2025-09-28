import requests
import json
from datetime import datetime

# APIs
COINGECKO_API = "https://api.coingecko.com/api/v3/coins/markets"
NEWS_API = "https://newsapi.org/v2/everything"  # Example for sentiment

# Parameters
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1,
    "sparkline": "false"
}

# Fetch market data
response = requests.get(COINGECKO_API, params=params)
coins = response.json()

# Simplified scoring (mock technical + sentiment)
top_coins = []
for i, coin in enumerate(coins[:20]):  # Top 20 for speed
    score = coin['market_cap_rank']  # Lower rank = higher score
    top_coins.append({
        "rank": i+1,
        "name": coin['name'],
        "symbol": coin['symbol'].upper(),
        "score": round(100 - score + 0.5, 2)  # Mock score
    })

top5 = sorted(top_coins, key=lambda x: x['score'], reverse=True)[:5]

# Save to JSON
output = {
    "last_updated": datetime.utcnow().isoformat() + "Z",
    "top5": top5
}

with open("update.json", "w") as f:
    json.dump(output, f, indent=4)
