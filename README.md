# 📊 Algo Trading Dashboard

A beginner-friendly **Streamlit app** that showcases **three powerful trading strategies** using live financial data. Perfect for fintech resumes, personal projects, or trading dashboards.

## 🚀 Features

### 1. 📈 SMA Crossover Backtest
- Implements a simple moving average crossover strategy.
- Lets users adjust short and long SMA periods.
- Generates buy/sell signals and plots chart for any stock ticker.

### 2. 💹 ETF Momentum Rotation
- Accepts multiple ETF tickers (e.g., `QQQ,SPY,IWM`).
- Calculates 60-day momentum to rank top-performing ETFs.
- Plots top 3 ETFs and offers CSV export.

### 3. 🔴 Live Signal Monitor
- Fetches live price data (1-min to hourly).
- Applies SMA20 and SMA50 crossover for real-time trading signals.
- Labels current market condition as BUY, SELL, or WAIT.

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
🧠 Tech Stack
🐍 Python

📈 Streamlit

🐼 Pandas

📉 yFinance

📊 Matplotlib

▶️ Run Locally

📄 License
MIT License

Made with ❤️ by @GunaVardhanaReddyT
