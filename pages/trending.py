import streamlit as st
import yfinance as yf
import pandas as pd

st.title('Trending Stocks')

@st.cache_data
def get_trending_stocks():
    # This is a placeholder for getting trending stocks.
    # For now, we will use a hardcoded list of stocks and sort by volume.
    # A better approach would be to use an API or a web scraper.

    tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "JPM", "JNJ", "V"]

    trending_stocks = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1d")

        if not hist.empty:
            trending_stocks.append({
                'Ticker': ticker,
                'Company Name': info.get('longName', 'N/A'),
                'Price': f"${hist['Close'][-1]:.2f}",
                'Change': f"${hist['Close'][-1] - hist['Open'][-1]:.2f}",
                '% Change': f"{(hist['Close'][-1] - hist['Open'][-1]) / hist['Open'][-1] * 100:.2f}%",
                'Volume': f"{hist['Volume'][-1]:,}"
            })

    # Sort by volume
    trending_stocks_df = pd.DataFrame(trending_stocks)
    trending_stocks_df['Volume_int'] = trending_stocks_df['Volume'].str.replace(',', '').astype(int)
    trending_stocks_df = trending_stocks_df.sort_values(by='Volume_int', ascending=False)
    trending_stocks_df = trending_stocks_df.drop(columns=['Volume_int'])

    return trending_stocks_df

st.write("Here are some of the most active stocks based on today's trading volume.")

trending_df = get_trending_stocks()

st.dataframe(trending_df, height=400)
