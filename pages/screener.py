import streamlit as st
import yfinance as yf
import pandas as pd

st.title('Stock Screener')

@st.cache_data
def get_sp500_tickers():
    # For now, we will use a hardcoded list of stocks.
    # A better approach would be to scrape the list from a reliable source like Wikipedia.
    return ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META", "JPM", "JNJ", "V", "PG", "UNH", "HD", "MA", "BAC", "DIS", "PFE", "KO", "XOM", "CSCO"]

@st.cache_data
def get_stock_data(tickers):
    stock_data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        stock_data.append({
            'Ticker': ticker,
            'Company Name': info.get('longName', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Industry': info.get('industry', 'N/A'),
            'Market Cap': info.get('marketCap', 0),
            'P/E Ratio': info.get('trailingPE', 0),
            'Dividend Yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
        })

    return pd.DataFrame(stock_data)

tickers = get_sp500_tickers()
df = get_stock_data(tickers)

st.sidebar.header('Filter Options')

# Sector filter
sectors = df['Sector'].unique()
selected_sectors = st.sidebar.multiselect('Sector', sectors, default=sectors)

# Market Cap filter
market_cap_min, market_cap_max = st.sidebar.slider(
    'Market Cap (in Billions)',
    min_value=0,
    max_value=int(df['Market Cap'].max() / 1e9),
    value=(0, int(df['Market Cap'].max() / 1e9))
)

# P/E Ratio filter
pe_ratio_min, pe_ratio_max = st.sidebar.slider(
    'P/E Ratio',
    min_value=0,
    max_value=int(df['P/E Ratio'].max()),
    value=(0, int(df['P/E Ratio'].max()))
)

# Dividend Yield filter
dividend_yield_min, dividend_yield_max = st.sidebar.slider(
    'Dividend Yield (%)',
    min_value=0.0,
    max_value=df['Dividend Yield'].max(),
    value=(0.0, df['Dividend Yield'].max())
)


# Apply filters
filtered_df = df[
    (df['Sector'].isin(selected_sectors)) &
    (df['Market Cap'] >= market_cap_min * 1e9) &
    (df['Market Cap'] <= market_cap_max * 1e9) &
    (df['P/E Ratio'] >= pe_ratio_min) &
    (df['P/E Ratio'] <= pe_ratio_max) &
    (df['Dividend Yield'] >= dividend_yield_min) &
    (df['Dividend Yield'] <= dividend_yield_max)
]

st.write(f"Showing {len(filtered_df)} of {len(df)} stocks")
st.dataframe(filtered_df)
