import streamlit as st
import yfinance as yf
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

st.title('News Sentiment Analysis')

@st.cache_resource
def download_vader():
    nltk.download('vader_lexicon')

download_vader()

# Load the stock data from the CSV file
df_stocks = pd.read_csv('pages/data.csv')
stocks = pd.Series(df_stocks.stock.values, index=df_stocks.Name).to_dict()

# Stock selection
selected_stock_name = st.selectbox('Select a stock for news sentiment analysis', list(stocks.keys()))
ticker = stocks[selected_stock_name]

@st.cache_data
def get_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    return news

news = get_news(ticker)

if news:
    analyzer = SentimentIntensityAnalyzer()

    for article in news:
        st.subheader(article['title'])
        st.write(f"**Source:** {article['publisher']} | **Link:** {article['link']}")

        sentiment = analyzer.polarity_scores(article['title'])

        # Display sentiment
        if sentiment['compound'] >= 0.05:
            st.success(f"Sentiment: Positive (Compound Score: {sentiment['compound']:.2f})")
        elif sentiment['compound'] <= -0.05:
            st.error(f"Sentiment: Negative (Compound Score: {sentiment['compound']:.2f})")
        else:
            st.warning(f"Sentiment: Neutral (Compound Score: {sentiment['compound']:.2f})")

        st.write("---")

else:
    st.write("No news available for this stock.")
