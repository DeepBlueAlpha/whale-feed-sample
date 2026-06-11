# Deep Blue Alpha — Whale Feed API

Sample code and documentation for the public API endpoints at [deepbluealpha.io](https://deepbluealpha.io) — real-time Ethereum whale tracking.

No API key required for the endpoints documented here. A full programmatic API (Leviathan tier, coming soon) will expose authenticated feed access; until then these public endpoints give you token-level aggregated flow data.

---

## Quick Start

```python
import requests

r = requests.get("https://deepbluealpha.io/api/top-tokens", params={"tf": "1H"})
tokens = r.json()

for t in tokens:
    net = t["buy_vol"] - t["sell_vol"]
    direction = "BUY" if net > 0 else "SELL"
    print(f"{t['token_symbol']:8}  net {direction}  ${abs(net):>12,.0f}  ({t['txn_count']} txns)")
```

```
ONDO       net SELL  $    50,731   (16 txns)
FET        net SELL  $   982,247   (12 txns)
LINK       net BUY   $   413,321   (22 txns)
CRV        net SELL  $   325,752   (34 txns)
...
```

---

## Endpoints

All endpoints are unauthenticated. Base URL: `https://deepbluealpha.io`

---

### `GET /api/top-tokens`

Top 20 tokens by whale volume over the selected window. Sorted by `volume` descending.

**Query parameters:**

| Param | Values | Description |
|-------|--------|-------------|
| `tf`  | `1H`, `24H` | Time window. `1H` = last 60 minutes. `24H` = last 24 hours. |

**Response — array of token objects:**

```json
[
  {
    "token_symbol": "ONDO",
    "token_address": "0xfaba6f8e4a5e8ab82f62fe7c39859fa577269be3",
    "volume": 3582639.49,
    "txn_count": 16,
    "buy_vol": 1765954.15,
    "sell_vol": 1816685.35
  },
  {
    "token_symbol": "LINK",
    "token_address": "0x514910771af9ca656af840dff83e8264ecf986ca",
    "volume": 1451757.49,
    "txn_count": 22,
    "buy_vol": 932539.20,
    "sell_vol": 519218.29
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `token_symbol` | string | Ticker symbol |
| `token_address` | string | ERC-20 contract address (checksummed) |
| `volume` | float | Total USD volume (`buy_vol + sell_vol`) |
| `txn_count` | int | Number of whale transactions in the window |
| `buy_vol` | float | USD volume of whale buy-side trades |
| `sell_vol` | float | USD volume of whale sell-side trades |

Net flow = `buy_vol - sell_vol`. Positive = net accumulation. Negative = net distribution.

---

### `GET /api/stats`

Aggregate whale activity across all tracked tokens for the selected window.

**Query parameters:**

| Param | Values | Description |
|-------|--------|-------------|
| `tf`  | `24H` | Time window (currently only `24H` is supported) |

**Response:**

```json
{
  "total_volume": 156876914.61,
  "buy_vol": 83300065.58,
  "sell_vol": 73576849.02,
  "trade_count": 12729,
  "tf": "24H"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total_volume` | float | Total USD volume tracked in the window |
| `buy_vol` | float | USD volume of buy-side whale trades |
| `sell_vol` | float | USD volume of sell-side whale trades |
| `trade_count` | int | Total number of tracked whale transactions |
| `tf` | string | Time frame echoed back from the request |

---

### `GET /api/price/{SYMBOL}`

CoinGecko price history for a token, served via DBA's cache.

**Path parameter:** `SYMBOL` — token ticker (e.g. `LINK`, `ONDO`, `AAVE`)

**Query parameters:**

| Param | Values | Description |
|-------|--------|-------------|
| `tf`  | `24h`, `1w`, `1mo`, `1yr` | Lookback window |

**Response:**

```json
{
  "has_data": true,
  "current_price": 7.79,
  "pct_change": 1.66,
  "prices": [
    [1781085332611, 7.67],
    [1781085626322, 7.69]
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `has_data` | bool | `false` if the symbol isn't tracked or CoinGecko has no data |
| `current_price` | float | Most recent price in USD |
| `pct_change` | float | Percentage change over the selected `tf` window |
| `prices` | array | `[[timestamp_ms, price_usd], ...]` — chronological OHLC-style price series |

---

## Python Examples

See the [`examples/`](./examples/) directory:

| File | What it does |
|------|-------------|
| [`whale_flow_monitor.py`](./examples/whale_flow_monitor.py) | Polls top tokens every 60 s; alerts when a token flips from net-buy to net-sell (or vice versa) |
| [`net_flow_summary.py`](./examples/net_flow_summary.py) | Fetches 24H stats and top tokens, prints a ranked summary table |

Both scripts require only the standard library plus `requests`:

```bash
pip install requests
python examples/net_flow_summary.py
```

---

## Full API Access — Coming Soon

The public endpoints above return token-level aggregated flow. The upcoming **Leviathan tier** ($99/mo) will expose a full authenticated API with per-transaction feed access, wallet-level data, and higher rate limits — suitable for algo systems and quantitative models.

Sign up at [deepbluealpha.io](https://deepbluealpha.io) to be notified when it launches. Free tier requires no signup.

---

## Pricing

| Tier | Monthly | Annual | Notes |
|------|---------|--------|-------|
| Free | $0 | $0 | No signup required |
| Pro Founder | $9.99 | $89 | Limited founder seats |
| Alpha Founder | $19.99 | $179 | Limited founder seats |
| Whale | $79 | — | Not yet open |
| Leviathan | $99 | — | Not yet open — includes API access |

Founder rates are locked for life once subscribed. Standard pricing applies after the founder cohort closes.

---

## Links

- Platform: [deepbluealpha.io](https://deepbluealpha.io)
- Live feed: [deepbluealpha.io/feed](https://deepbluealpha.io/feed)
- Whale wallet leaderboard: [deepbluealpha.io/wallets](https://deepbluealpha.io/wallets)
- X: [@DeepBlueAlpha](https://x.com/DeepBlueAlpha)
- Telegram: [t.me/DeepBlueAlphaIO](https://t.me/DeepBlueAlphaIO)
