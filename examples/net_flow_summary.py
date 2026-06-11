"""
net_flow_summary.py
-------------------
Fetches 24H aggregate stats and the top-20 tokens by whale volume,
then prints a ranked summary table with net flow and buy/sell split.

No API key required.
Requires: pip install requests
"""

import requests

BASE = "https://deepbluealpha.io"


def fetch_stats() -> dict:
    resp = requests.get(f"{BASE}/api/stats", params={"tf": "24H"}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_top_tokens() -> list[dict]:
    resp = requests.get(f"{BASE}/api/top-tokens", params={"tf": "24H"}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fmt_usd(v: float) -> str:
    if abs(v) >= 1_000_000:
        return f"${v/1_000_000:.2f}M"
    if abs(v) >= 1_000:
        return f"${v/1_000:.1f}K"
    return f"${v:.0f}"


def fmt_pct(buy: float, sell: float) -> str:
    total = buy + sell
    if total == 0:
        return " 50% buy"
    pct = buy / total * 100
    return f"{pct:4.0f}% buy"


def main():
    stats = fetch_stats()
    tokens = fetch_top_tokens()

    total = stats["total_volume"]
    buy = stats["buy_vol"]
    sell = stats["sell_vol"]
    net = buy - sell
    net_sign = "+" if net >= 0 else "-"

    print("=" * 70)
    print("Deep Blue Alpha — 24H Whale Flow Summary")
    print("=" * 70)
    print(f"  Total volume : {fmt_usd(total)}")
    print(f"  Buy volume   : {fmt_usd(buy)}")
    print(f"  Sell volume  : {fmt_usd(sell)}")
    print(f"  Net flow     : {net_sign}{fmt_usd(abs(net))}")
    print(f"  Transactions : {stats['trade_count']:,}")
    print("=" * 70)
    print()

    # Ranked table
    header = f"{'#':>2}  {'TOKEN':<8}  {'VOL':>10}  {'BUY':>10}  {'SELL':>10}  {'NET':>10}  {'BUY%':>8}  {'TXNS':>5}"
    print(header)
    print("-" * len(header))

    for i, t in enumerate(tokens, 1):
        b, s = t["buy_vol"], t["sell_vol"]
        net_tok = b - s
        net_str = ("+" if net_tok >= 0 else "") + fmt_usd(net_tok)
        direction = "▲" if net_tok >= 0 else "▼"
        print(
            f"{i:>2}  {t['token_symbol']:<8}  "
            f"{fmt_usd(t['volume']):>10}  "
            f"{fmt_usd(b):>10}  "
            f"{fmt_usd(s):>10}  "
            f"{direction} {net_str:>9}  "
            f"{fmt_pct(b, s):>8}  "
            f"{t['txn_count']:>5}"
        )

    print()
    net_buy_count = sum(1 for t in tokens if t["buy_vol"] >= t["sell_vol"])
    print(f"Net buyers: {net_buy_count}/{len(tokens)} tokens in top 20")
    print(f"\nData: {BASE}  |  @DeepBlueAlpha")


if __name__ == "__main__":
    main()
