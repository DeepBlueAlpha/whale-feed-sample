"""
whale_flow_monitor.py
---------------------
Polls deepbluealpha.io/api/top-tokens every 60 seconds and prints an alert
whenever a token flips its net-flow direction (buy -> sell or sell -> buy).

No API key required.
Requires: pip install requests
"""

import time
import requests

API_URL = "https://deepbluealpha.io/api/top-tokens"
POLL_INTERVAL = 60  # seconds


def fetch_top_tokens(tf: str = "1H") -> list[dict]:
    resp = requests.get(API_URL, params={"tf": tf}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def net_direction(token: dict) -> str:
    """Return 'BUY' if net buyers, 'SELL' if net sellers."""
    return "BUY" if token["buy_vol"] >= token["sell_vol"] else "SELL"


def format_net(token: dict) -> str:
    net = token["buy_vol"] - token["sell_vol"]
    sign = "+" if net >= 0 else "-"
    return f"{sign}${abs(net):,.0f}"


def main():
    print("Deep Blue Alpha — Whale Flow Monitor")
    print(f"Polling /api/top-tokens?tf=1H every {POLL_INTERVAL}s")
    print("Press Ctrl+C to stop.\n")

    prev_directions: dict[str, str] = {}

    while True:
        try:
            tokens = fetch_top_tokens("1H")
        except requests.RequestException as e:
            print(f"[{time.strftime('%H:%M:%S')}] fetch error: {e}")
            time.sleep(POLL_INTERVAL)
            continue

        current_directions = {t["token_symbol"]: net_direction(t) for t in tokens}

        for token in tokens:
            sym = token["token_symbol"]
            direction = current_directions[sym]
            prev = prev_directions.get(sym)

            if prev is not None and prev != direction:
                net_str = format_net(token)
                print(
                    f"[{time.strftime('%H:%M:%S')}]  FLIP  {sym:8}  "
                    f"{prev} -> {direction}  net {net_str}  "
                    f"({token['txn_count']} txns, ${token['volume']:,.0f} vol)"
                )

        prev_directions = current_directions

        # Print a periodic summary so the terminal isn't silent during quiet periods
        print(f"\n[{time.strftime('%H:%M:%S')}] 1H snapshot — top 5 by volume:")
        for t in tokens[:5]:
            d = net_direction(t)
            arrow = "▲" if d == "BUY" else "▼"
            print(
                f"  {arrow} {t['token_symbol']:8}  vol ${t['volume']:>12,.0f}  "
                f"net {format_net(t):>14}  {t['txn_count']} txns"
            )

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
