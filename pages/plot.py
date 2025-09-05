import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
import streamlit as st
import pandas as pd
import pandas_ta as ta

# Load the stock data from the CSV file
df = pd.read_csv('pages/data.csv')
dic = pd.Series(df.stock.values, index=df.Name).to_dict()

today = date.today()

# Set the start and end date
start_date = '1990-01-01'
end_date = st.date_input("End Date", value=today, max_value=today) # Set default to today

#Set the ticker
if "ticker" in st.session_state:
  ticker_symbol = st.session_state.ticker # Renamed to avoid conflict with `ticker` object
else:
  tic = st.selectbox("Select a Stock", list(dic.keys())) # Changed prompt
  ticker_symbol = dic[tic]

st.title(f"Stock Analysis for {ticker_symbol}")

# Get the data
data = yf.download(ticker_symbol, start_date, end_date)

if not data.empty:
    st.subheader("Historical Stock Prices")
    st.write(data.tail()) # Display last 5 rows

    # Calculate technical indicators
    data.ta.bbands(append=True)
    data.ta.rsi(append=True)
    data.ta.macd(append=True)


    # Plot adjusted close price data with Bollinger Bands
    fig, ax = plt.subplots(figsize=(10, 6)) # Increased figure size
    ax.plot(data['Close'], label='Close Price')
    ax.plot(data['BBL_20_2.0'], label='Lower Bollinger Band', linestyle='--')
    ax.plot(data['BBM_20_2.0'], label='Middle Bollinger Band', linestyle='--')
    ax.plot(data['BBU_20_2.0'], label='Upper Bollinger Band', linestyle='--')
    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted Close Price')
    ax.set_title(f'{ticker_symbol} Adjusted Close Price Data with Bollinger Bands')
    ax.legend()
    st.pyplot(fig)

    # Add more plots and data:
    st.subheader("Volume Data")
    fig_vol, ax_vol = plt.subplots(figsize=(10, 4))
    ax_vol.plot(data['Volume'], color='orange')
    ax_vol.set_xlabel('Date')
    ax_vol.set_ylabel('Volume')
    ax_vol.set_title(f'{ticker_symbol} Trading Volume')
    st.pyplot(fig_vol)

    # RSI
    st.subheader("Relative Strength Index (RSI)")
    fig_rsi, ax_rsi = plt.subplots(figsize=(10, 4))
    ax_rsi.plot(data['RSI_14'], color='purple')
    ax_rsi.axhline(70, linestyle='--', color='red')
    ax_rsi.axhline(30, linestyle='--', color='green')
    ax_rsi.set_xlabel('Date')
    ax_rsi.set_ylabel('RSI')
    ax_rsi.set_title(f'{ticker_symbol} RSI')
    st.pyplot(fig_rsi)

    # MACD
    st.subheader("Moving Average Convergence Divergence (MACD)")
    fig_macd, ax_macd = plt.subplots(figsize=(10, 4))
    ax_macd.plot(data['MACD_12_26_9'], label='MACD', color='blue')
    ax_macd.plot(data['MACDs_12_26_9'], label='Signal Line', color='red')
    ax_macd.set_xlabel('Date')
    ax_macd.set_ylabel('MACD')
    ax_macd.set_title(f'{ticker_symbol} MACD')
    ax_macd.legend()
    st.pyplot(fig_macd)


    # Dividends and Stock Splits
    st.subheader("Dividends and Stock Splits")
    stock = yf.Ticker(ticker_symbol)
    dividends = stock.dividends
    splits = stock.splits

    if not dividends.empty:
        st.write("Dividends:")
        st.dataframe(dividends)
    else:
        st.write("No dividend data available for this stock.")

    if not splits.empty:
        st.write("Stock Splits:")
        st.dataframe(splits)
    else:
        st.write("No stock split data available for this stock.")

    # Financial Statements (Income Statement, Balance Sheet, Cash Flow)
    st.subheader("Financial Statements")

    try:
        st.write("### Income Statement (Annual)")
        st.dataframe(stock.financials)
    except Exception as e:
        st.write(f"Could not retrieve annual income statement: {e}")

    try:
        st.write("### Balance Sheet (Annual)")
        st.dataframe(stock.balance_sheet)
    except Exception as e:
        st.write(f"Could not retrieve annual balance sheet: {e}")

    try:
        st.write("### Cash Flow Statement (Annual)")
        st.dataframe(stock.cashflow)
    except Exception as e:
        st.write(f"Could not retrieve annual cash flow statement: {e}")

    # Quarterly Financials
    st.subheader("Quarterly Financials")
    try:
        st.write("### Income Statement (Quarterly)")
        st.dataframe(stock.quarterly_financials)
    except Exception as e:
        st.write(f"Could not retrieve quarterly income statement: {e}")

    try:
        st.write("### Balance Sheet (Quarterly)")
        st.dataframe(stock.quarterly_balance_sheet)
    except Exception as e:
        st.write(f"Could not retrieve quarterly balance sheet: {e}")

    try:
        st.write("### Cash Flow Statement (Quarterly)")
        st.dataframe(stock.quarterly_cashflow)
    except Exception as e:
        st.write(f"Could not retrieve quarterly cash flow statement: {e}")

    # Institutional Shareholders
    st.subheader("Institutional Shareholders")
    try:
        st.dataframe(stock.institutional_holders)
    except Exception as e:
        st.write(f"Could not retrieve institutional holders: {e}")

    # Analyst Recommendations
    st.subheader("Analyst Recommendations")
    try:
        st.dataframe(stock.recommendations)
    except Exception as e:
        st.write(f"Could not retrieve analyst recommendations: {e}")

    # Company Info (Summary)
    st.subheader("Company Information")
    try:
        info = stock.info
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Full Time Employees:** {info.get('fullTimeEmployees', 'N/A')}")
        st.write(f"**Website:** {info.get('website', 'N/A')}")
        st.write("**Summary:**")
        st.write(info.get('longBusinessSummary', 'N/A'))
    except Exception as e:
        st.write(f"Could not retrieve company information: {e}")

else:
    st.warning(f"Could not retrieve data for {ticker_symbol}. Please check the ticker symbol or date range.")
