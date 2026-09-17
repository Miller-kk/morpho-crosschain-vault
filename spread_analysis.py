"""Daily organic-APY spread: HyperEVM USDC vaults vs Base Steakhouse Prime USDC.

Inputs: Harvest Finance daily realized-APY history CSVs
  https://harvest.finance/history/usdc-morpho-gauntlet-hyperevm.csv
  https://harvest.finance/history/usdc-morpho-felix-hyperevm.csv
  https://harvest.finance/history/usdc-morpho-steakhouse-prime-v2-base.csv
Each has columns date,apy (percent). Harvest samples most but not every day;
series are forward-filled onto a daily grid before computing spreads.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load(path):
    return pd.read_csv(path, parse_dates=["date"]).set_index("date")["apy"]

def build(gauntlet, felix, base, start="2025-11-20", end="2026-09-14"):
    idx = pd.date_range(start, end)
    df = pd.DataFrame({
        "gauntlet_hyperevm": load(gauntlet).reindex(idx).ffill(),
        "felix_hyperevm":    load(felix).reindex(idx).ffill(),
        "base_steak_prime":  load(base).reindex(idx).ffill(),
    })
    df["spread_g"] = (df.gauntlet_hyperevm - df.base_steak_prime) * 100  # bp
    df["spread_f"] = (df.felix_hyperevm - df.base_steak_prime) * 100
    df.index.name = "date"
    return df

def stats(s, name):
    for w in (30, 90, 180, len(s)):
        x = s[-w:]
        print(f"{name} last {w}d: mean {x.mean():.0f} bp, days>=100bp {(x>=100).sum()}/{w}, days<0 {(x<0).sum()}")

def streak(s, th):
    best = cur = 0
    for v in s:
        cur = cur + 1 if v >= th else 0
        best = max(best, cur)
    return best

def chart(df, out="hyperevm_vs_base_spread.png"):
    fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [1.2, 1]})
    ax[0].plot(df.index, df.gauntlet_hyperevm, label="Gauntlet USDC – HyperEVM", lw=1.4, color="#d62728")
    ax[0].plot(df.index, df.felix_hyperevm, label="Felix USDC Frontier – HyperEVM", lw=1.4, color="#ff7f0e")
    ax[0].plot(df.index, df.base_steak_prime, label="Steakhouse Prime USDC – Base (baseline)", lw=1.6, color="#1f77b4")
    ax[0].set_ylabel("Realized APY (%)"); ax[0].legend(loc="upper right", fontsize=9); ax[0].grid(alpha=.3)
    ax[0].set_title("USDC vault yield: HyperEVM vs Base, daily (Harvest index, forward-filled)", fontsize=11)
    r = df.spread_g.rolling(30).mean()
    ax[1].bar(df.index, df.spread_g, width=1, color="#d62728", alpha=.35, label="Daily spread, Gauntlet − Base")
    ax[1].plot(df.index, r, color="#d62728", lw=2, label="30-day rolling mean")
    ax[1].axhline(100, color="k", ls="--", lw=.8); ax[1].axhline(0, color="k", lw=.8)
    ax[1].set_ylabel("Spread (bp)"); ax[1].legend(loc="upper left", fontsize=9); ax[1].grid(alpha=.3)
    ax[1].set_ylim(-250, 450)
    plt.tight_layout(); plt.savefig(out, dpi=150)

if __name__ == "__main__":
    df = pd.read_csv("hyperevm_vs_base_daily.csv", index_col=0, parse_dates=True)
    stats(df.spread_g, "Gauntlet-Base"); stats(df.spread_f, "Felix-Base")
    print(df.resample("ME").mean().round(2))
    for th in (0, 50, 100):
        print(f"longest streak >={th}bp: gauntlet {streak(df.spread_g, th)}d, felix {streak(df.spread_f, th)}d")
    chart(df)
