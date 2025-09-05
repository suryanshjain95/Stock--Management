import streamlit as st
import yfinance as yf
import pandas as pd

st.title('Buy/Sell Suggestion')

# Load the stock data from the CSV file
df_stocks = pd.read_csv('pages/data.csv')
stocks = pd.Series(df_stocks.stock.values, index=df_stocks.Name).to_dict()

# Stock selection
selected_stock_name = st.selectbox('Select a stock for suggestion', list(stocks.keys()))
ticker = stocks[selected_stock_name]

@st.cache_data
def get_recommendations(ticker):
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations
    return recommendations

recommendations = get_recommendations(ticker)

if recommendations is not None and not recommendations.empty:
    st.subheader(f'Analyst Recommendations for {ticker}')
    st.dataframe(recommendations)

    # Simple suggestion logic based on the latest recommendations
    latest_recommendations = recommendations['To Grade'].str.lower()

    buy_ratings = latest_recommendations.str.contains('buy|outperform|overweight').sum()
    sell_ratings = latest_recommendations.str.contains('sell|underperform|underweight').sum()
    hold_ratings = latest_recommendations.str.contains('hold|neutral|equal-weight').sum()

    st.subheader('Recommendation Summary')
    st.write(f"Buy Ratings: {buy_ratings}")
    st.write(f"Sell Ratings: {sell_ratings}")
    st.write(f"Hold Ratings: {hold_ratings}")

    if buy_ratings > sell_ratings and buy_ratings > hold_ratings:
        st.success('Suggestion: BUY')
    elif sell_ratings > buy_ratings and sell_ratings > hold_ratings:
        st.error('Suggestion: SELL')
    else:
        st.warning('Suggestion: HOLD')

else:
    st.write("No analyst recommendations available for this stock.")
