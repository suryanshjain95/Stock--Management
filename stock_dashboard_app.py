import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

# ----------- PAGE CONFIG -----------
st.set_page_config(
    page_title="Stock Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------- DATA -----------
default_stocks = {
    "Company": ["Apple", "Microsoft", "Google", "Amazon", "Tesla", "Meta"],
    "Ticker": ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META"]
}
df = pd.DataFrame(default_stocks)

# ----------- FUNCTIONS -----------
def get_stock_change(ticker):
    today = date.today()
    start_date = '2020-01-01'
    data = yf.download(ticker, start=start_date, end=today)
    if data.empty:
        return "N/A", "N/A"
    close_price = data["Close"].iloc[-1]
    open_price = data["Open"].iloc[-1]
    change = close_price - open_price
    pct_change = (change / open_price) * 100
    return f"{pct_change:.2f}%", f"{change:.2f}"

def plot_stock(ticker):
    today = date.today()
    data = yf.download(ticker, start="2020-01-01", end=today)
    if data.empty:
        st.warning("No data available for this ticker.")
        return
    fig, ax = plt.subplots()
    ax.plot(data.index, data["Close"], color="cyan", label="Close Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.set_title(f"{ticker} Closing Price History")
    ax.legend()
    st.pyplot(fig)

# ----------- MAIN UI -----------
st.title("💹 Stock Dashboard")

search_ticker = st.text_input("Search ticker (e.g., NVDA, NFLX, AMD):").upper()

if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = None

if search_ticker:
    st.session_state.selected_ticker = search_ticker

st.subheader("Popular Stocks")

num_rows = len(df)
cols = st.columns(4)

for i, row in df.iterrows():
    col = cols[i % 4]
    with col:
        pct, change = get_stock_change(row["Ticker"])
        if st.button(row["Company"], key=row["Ticker"]):
            st.session_state.selected_ticker = row["Ticker"]
        st.metric(label=row["Ticker"], value=pct, delta=change)

st.divider()

if st.session_state.selected_ticker:
    ticker = st.session_state.selected_ticker
    st.subheader(f"📊 Detailed View for {ticker}")
    plot_stock(ticker)
    data = yf.download(ticker, start="2020-01-01")
    if not data.empty:
        st.write("Recent Data")
        st.dataframe(data.tail(10))
else:
    st.info("Search or select a company to view stock details.")
