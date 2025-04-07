import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("📈 Algo Trading Dashboard")

option = st.sidebar.radio("Select a Strategy", (
    "SMA Crossover Backtest",
    "ETF Momentum Rotation",
    "Live Signal Monitor"
))


if option == "SMA Crossover Backtest":
    st.header("SMA Crossover Strategy")
    ticker = st.text_input("Enter Stock Symbol", "AAPL")
    short = st.slider("Short SMA", 5, 50, 20)
    long = st.slider("Long SMA", 20, 200, 50)

    try:
        data = yf.download(ticker, period="1y")

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data["SMA_Short"] = data["Close"].rolling(window=short).mean()
        data["SMA_Long"] = data["Close"].rolling(window=long).mean()
        data["Signal"] = 0
        data.loc[data.index[short:], "Signal"] = (
            data["SMA_Short"][short:] > data["SMA_Long"][short:]
        ).astype(int)
        data["Position"] = data["Signal"].diff()

        st.line_chart(data[["Close", "SMA_Short", "SMA_Long"]])

        buy_signals = data[data["Position"] == 1.0]
        sell_signals = data[data["Position"] == -1.0]

        st.success(f"Buy signals: {len(buy_signals)} | Sell signals: {len(sell_signals)}")
    except Exception:
        st.error("🚨 Oops! Something went wrong while fetching or calculating SMA crossover. Please check the ticker and try again.")

elif option == "ETF Momentum Rotation":
    st.header("ETF Momentum Rotation")
    etfs_input = st.text_input("Enter ETF tickers (comma-separated)", "QQQ,SPY,IWM,EFA,EEM")
    etfs = [etf.strip().upper() for etf in etfs_input.split(',') if etf.strip()]

    try:
        data = yf.download(etfs, period="6mo", group_by="ticker")

        adj_close = pd.DataFrame()
        for etf in etfs:
            if etf in data and "Adj Close" in data[etf]:
                adj_close[etf] = data[etf]["Adj Close"]

        if len(adj_close) > 60:
            momentum = adj_close.pct_change(60).iloc[-1].sort_values(ascending=False)
            top_etfs = momentum.head(3)

            st.subheader("Top Momentum ETFs")
            st.write(top_etfs)
            st.line_chart(adj_close[top_etfs.index])

            csv = top_etfs.to_csv().encode("utf-8")
            st.download_button("Download Top ETFs as CSV", csv, "top_etfs.csv", "text/csv")

        else:
            st.warning("⚠️ Not enough historical data to compute 60-day momentum. Try different ETFs or increase the period.")

    except Exception:
        st.error("🚨 Failed to fetch or process ETF momentum data. Please verify the ticker symbols and your internet connection.")

elif option == "Live Signal Monitor":
    st.header("Live Price Monitor + Signal")
    ticker = st.text_input("Stock Ticker", "AAPL")
    interval = st.selectbox("Interval", ["1m", "5m", "15m", "30m", "1h"], index=2)

    try:
        data = yf.download(ticker, period="7d", interval=interval)

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data["SMA20"] = data["Close"].rolling(20).mean()
        data["SMA50"] = data["Close"].rolling(50).mean()

        signal = "WAIT"
        if data["SMA20"].iloc[-1] > data["SMA50"].iloc[-1]:
            signal = "BUY"
        elif data["SMA20"].iloc[-1] < data["SMA50"].iloc[-1]:
            signal = "SELL"

        st.line_chart(data[["Close", "SMA20", "SMA50"]])
        st.success(f"Current Signal: {signal}")
    except Exception:
        st.error("🚨 Error fetching live data or calculating signals. Please double-check the ticker and try again.")
