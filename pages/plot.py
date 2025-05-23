import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
import streamlit as st
import pandas as pd # Import pandas

dic={"Apple":"AAPL", "Tesla":"TSLA", "Microsoft":"MSFT","Mullen":"MULN","Bit Brother":"BETSF","Paragon":"PRGNF","Smart for Life":"SMFL","Wearable Devices":"WLDS","Kohl's Corporation":"KSS","Affymax":"AFFY","Wolfspeed":"WOLF","Beyond Meat":"BYND","American Rebel":"AREB","Entegris":"ENTG","CAVA Group":"CAVA","Amcor":"AMCR","Tapestry":"TPR","CarMax":"KMX","Pool Corporation":"POOL","Exelixis":"EXEL"}

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

    # Plot adjusted close price data
    fig, ax = plt.subplots(figsize=(10, 6)) # Increased figure size
    ax.plot(data['Close'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted Close Price')
    ax.set_title(f'{ticker_symbol} Adjusted Close Price Data')
    st.pyplot(fig)

    # Add more plots and data:
    st.subheader("Volume Data")
    fig_vol, ax_vol = plt.subplots(figsize=(10, 4))
    ax_vol.plot(data['Volume'], color='orange')
    ax_vol.set_xlabel('Date')
    ax_vol.set_ylabel('Volume')
    ax_vol.set_title(f'{ticker_symbol} Trading Volume')
    st.pyplot(fig_vol)

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
