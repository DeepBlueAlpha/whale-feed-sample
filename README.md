# 🐳 Deep Blue Alpha — Whale Feed API Sample

Sample responses, Python snippets, and integration examples for the [Deep Blue Alpha](https://deepbluealpha.io) Ethereum whale feed API.

> **Platform:** [deepbluealpha.io](https://deepbluealpha.io) | **Free tier:** no API key required for public feed

---

## 🚀 Quick Start

```python
import requests

# Public feed — no auth required (free tier, 24h window)
r = requests.get("https://deepbluealpha.io/api/feed")
data = r.json()

for move in data["data"]:
    print(move['wallet'][:8], move['token'], move['action'], move['value_usd'])
```

---

## 📡 API Endpoints

### GET /api/feed — Public Whale Feed

No API key required. Returns the latest whale moves from the past 24 hours.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| limit | int | 50 | Number of results (max 100 free) |
| action | string | all | Filter: accumulate, distribute, all |
| min_usd | int | 50000 | Minimum USD value |

**Sample response:**

```json
{
  "status": "ok",
  "timestamp": "2026-04-10T14:23:07Z",
  "fear_greed_index": 14,
  "eth_price_usd": 2249.92,
  "data": [
    {
      "id": "wm_9f3a1b2c",
      "wallet": "0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE",
      "wallet_label": "Whale #441",
      "wallet_age_days": 1847,
      "token": "SCFG",
      "action": "accumulate",
      "tx_count": 7,
      "value_usd": 284000,
      "signal_score": 87
    }
  ]
}
```

---

### GET /api/scoreboard — 30-Day Scoreboard

```json
{
  "hit_rate": 0.71,
  "wins": 84,
  "big_wins": 20,
  "losses": 34,
  "top_picks": [
    {"token": "SCFG",  "return_pct": 35.8, "outcome": "win"},
    {"token": "BASER", "return_pct": 15.6, "outcome": "win"},
    {"token": "COMP",  "return_pct": 12.6, "outcome": "win"}
  ]
}
```

---

## 🐍 Python Examples

### Filter high-conviction signals

```python
import requests

def get_high_conviction(min_score=80, min_usd=100_000):
    r = requests.get("https://deepbluealpha.io/api/feed", params={
        "action": "accumulate",
        "min_usd": min_usd,
        "limit": 100
    })
    moves = r.json()["data"]
    return [m for m in moves if m["signal_score"] >= min_score]
```

### Discord alert bot

```python
import requests, time

WEBHOOK = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
seen = set()

def check_feed():
    moves = requests.get(
        "https://deepbluealpha.io/api/feed?action=accumulate&min_usd=200000"
    ).json()["data"]
    for m in moves:
        if m["id"] not in seen and m["signal_score"] >= 75:
            seen.add(m["id"])
            msg = "WHALE: " + m['token'] + " | $" + str(m['value_usd']) + " | Score: " + str(m['signal_score'])
            requests.post(WEBHOOK, json={"content": msg})

while True:
    check_feed()
    time.sleep(60)
```

---

## 📊 Signal Score (0–100)

| Factor | Weight | Description |
|--------|--------|-------------|
| Wallet age | 20% | Older wallets = more credibility |
| TX pattern | 25% | Batch buys over days = stronger signal |
| Position size | 20% | Larger = higher conviction |
| Token liquidity | 15% | Lower liq = higher alpha potential |
| Wallet history | 20% | Past accuracy of this wallet |

80+ = High conviction | 60–79 = Watch | Below 60 = Noise

---

## 🔑 API Tiers

| Tier | Key | Rate Limit | History |
|------|-----|------------|---------|
| Free | No | 100/day | 24h |
| Alpha $19/mo | Yes | 1,000/day | 7 days |
| Whale $49/mo | Yes | 10,000/day | 30 days |
| Leviathan $99/mo | Yes | Unlimited | Full |

Get your key: [deepbluealpha.io](https://deepbluealpha.io)

## 📄 License

MIT — free to use, modify, and build on.

*Built by [@DeepBlueAlpha](https://x.com/DeepBlueAlpha)*
