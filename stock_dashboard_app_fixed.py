# stock_dashboard_app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit settings
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# Dark theme for Matplotlib
plt.style.use("dark_background")

# --- Sidebar ---
st.sidebar.title("📈 Stock Dashboard")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g. AAPL, TSLA, INFY.NS)", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.Timestamp.today())

# Fetch data
@st.cache_data
def get_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            st.warning("⚠️ No data found for that ticker symbol.")
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

data = get_data(ticker, start_date, end_date)

if not data.empty:
    st.title(f"💹 {ticker} Stock Analysis")

    # --- Overview metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Close", f"${data['Close'][-1]:.2f}")
    col2.metric("Daily High", f"${data['High'][-1]:.2f}")
    col3.metric("Daily Low", f"${data['Low'][-1]:.2f}")

    # --- Price Chart ---
    st.subheader("Price Movement")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data["Close"], label="Close Price", color="#00FFAA")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    st.pyplot(fig)

    # --- Moving Averages ---
    st.subheader("Moving Averages")
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(data.index, data["Close"], label="Close", color="#00FFAA")
    ax2.plot(data.index, data["MA20"], label="20-Day MA", color="orange")
    ax2.plot(data.index, data["MA50"], label="50-Day MA", color="red")
    ax2.legend()
    st.pyplot(fig2)

    # --- Volume Chart ---
    st.subheader("Volume Traded")
    fig3, ax3 = plt.subplots(figsize=(10, 3))
    ax3.bar(data.index, data["Volume"], color="#3399FF")
    ax3.set_ylabel("Volume")
    st.pyplot(fig3)

    # --- Data Table ---
    st.subheader("Raw Data")
    st.dataframe(data.tail(20))

else:
    st.info("👈 Enter a valid stock ticker in the sidebar to begin.")

# Footer
st.markdown("---")
st.markdown("⚡ Built with [Streamlit](https://streamlit.io), [yfinance](https://pypi.org/project/yfinance), and [Matplotlib](https://matplotlib.org)")
