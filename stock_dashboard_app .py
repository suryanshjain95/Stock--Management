
import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="📈 Stock Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

plt.style.use('dark_background')

# --- Helper Functions ---
def download_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data

def plot_price_chart(data, ticker):
    data['SMA20'] = data['Close'].rolling(20).mean()
    data['SMA50'] = data['Close'].rolling(50).mean()
    data['SMA200'] = data['Close'].rolling(200).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label='Close', color='cyan', linewidth=1.5)
    ax.plot(data.index, data['SMA20'], label='SMA20', linestyle='--')
    ax.plot(data.index, data['SMA50'], label='SMA50', linestyle='--')
    ax.plot(data.index, data['SMA200'], label='SMA200', linestyle='--')
    ax.fill_between(data.index, data['Low'], data['High'], color='gray', alpha=0.2, label='Daily Range')
    ax.set_title(f"{ticker} Stock Prices with Moving Averages", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(alpha=0.4)
    st.pyplot(fig)

def plot_volume_chart(data, ticker):
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.bar(data.index, data['Volume'], color='purple', alpha=0.6)
    ax.set_title(f"{ticker} Trading Volume", fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")
    st.pyplot(fig)

def compare_stocks(tickers, start, end):
    data = yf.download(tickers, start=start, end=end)['Close']
    normalized = data / data.iloc[0] * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in tickers:
        ax.plot(normalized.index, normalized[ticker], label=ticker)
    ax.set_title("Stock Performance Comparison (Normalized to 100%)", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Performance (%)")
    ax.legend()
    ax.grid(alpha=0.4)
    st.pyplot(fig)

# --- Sidebar ---
st.sidebar.header("⚙️ Controls")

option = st.sidebar.radio("Choose Mode:", ["Single Stock", "Compare Stocks"])
default_start = datetime.date.today() - datetime.timedelta(days=365)
default_end = datetime.date.today()

if option == "Single Stock":
    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, INFY.NS)", "AAPL").upper()
    start = st.sidebar.date_input("Start Date", default_start)
    end = st.sidebar.date_input("End Date", default_end)

    if st.sidebar.button("Fetch Data"):
        with st.spinner("Downloading data..."):
            data = download_data(ticker, start, end)

        if data.empty:
            st.error("❌ No data found! Check ticker or date range.")
        else:
            st.success(f"✅ Data for {ticker} loaded successfully!")

            st.subheader(f"📊 {ticker} Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Mean Close", f"${data['Close'].mean():.2f}")
            col2.metric("Highest", f"${data['Close'].max():.2f}")
            col3.metric("Lowest", f"${data['Close'].min():.2f}")
            col4.metric("Volatility", f"{data['Close'].std():.2f}")

            st.markdown("---")
            plot_price_chart(data, ticker)
            plot_volume_chart(data, ticker)

elif option == "Compare Stocks":
    tickers_input = st.sidebar.text_input("Enter tickers separated by commas", "AAPL,TSLA,MSFT")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    start = st.sidebar.date_input("Start Date", default_start)
    end = st.sidebar.date_input("End Date", default_end)

    if st.sidebar.button("Compare"):
        with st.spinner("Fetching comparison data..."):
            compare_stocks(tickers, start, end)
