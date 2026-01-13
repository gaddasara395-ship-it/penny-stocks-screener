import yfinance as yf
import pandas as pd
import numpy as np

# List of NSE penny stocks
stocks = [
    "RPOWER.NS",
    "YESBANK.NS",
    "SUZLON.NS",
    "JPPOWER.NS",
    "IDEA.NS",
    "PNB.NS"
]

results = []

print("🔍 Screening penny stocks...\n")

for stock in stocks:
    data = yf.download(stock, period="6mo", interval="1d", progress=False)

    if data.empty:
        continue

    close_prices = data["Close"].squeeze()
    volumes = data["Volume"].squeeze()

    current_price = close_prices.iloc[-1].item()
    avg_volume = volumes.mean().item()



    # 1-month return (approx 22 trading days)
    if len(close_prices) > 22:
        monthly_return = (
            (close_prices.iloc[-1] - close_prices.iloc[-22])
            / close_prices.iloc[-22]
        ) * 100
    else:
        monthly_return = 0

    # Screening conditions
    if current_price < 100 and avg_volume > 100000:
        results.append({
            "Stock": stock,
            "Price (₹)": round(current_price, 2),
            "Avg Volume": int(avg_volume),
            "1M Return (%)": round(monthly_return, 2)
        })

# Display result
df = pd.DataFrame(results)

print("📊 Penny Stocks Screener Result:\n")
if not df.empty:
    print(df)
else:
    print("No stocks matched the criteria.")
    df.to_excel("penny_stock_results.xlsx", index=False)
print("\n📁 Results saved as penny_stock_results.xlsx")

