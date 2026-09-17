# Cross-chain USDC vault on Morpho Vault V2 via CCTP

Data and analysis behind the Morpho forum post
*"A cross-chain USDC vault on Vault V2 via CCTP: following borrow demand across chains"*.

## What is here

| File | What |
|---|---|
| `hyperevm_vs_base_daily.csv` | Daily realized APY (%) for Gauntlet USDC (HyperEVM), Felix USDC Frontier (HyperEVM) and Steakhouse Prime USDC (Base), Nov 2025 – Sep 2026, forward-filled to a daily grid, plus spreads in bp |
| `spread_analysis.py` | Reproduces the persistence statistics, monthly means, streaks and the chart |
| `hyperevm_vs_base_spread.png` | The chart in the post |

## Sources

- Daily APY series: Harvest Finance history endpoints (`harvest.finance/history/<vault>.csv`). Share-price based; includes autocompounded MORPHO rewards, so the Base baseline overstates organic yield by roughly 50–100 bp in Nov 2025 – Jan 2026.
- Organic cross-check: Morpho REST API, `api.morpho.org/v0/blue/markets/8453:0x9103c3b4…/apy-averages` (Base cbBTC/USDC 86%: 30d 4.35%, 90d 4.40%, 1y 4.96%).
- Chain TVL, fees and incentives: DefiLlama protocol page for Morpho, 15 Sep 2026.
- Vault-level snapshots: Morpho app vault and market pages, 15 Sep 2026.

## Status

Stage 0: research. The CrossChainAdapter and RemoteExecutor contracts will be published here before the stage-1 pilot deployment.

## Reproduce

```
pip install pandas matplotlib
python spread_analysis.py
```
