import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
import pandas as pd

st.title('Stock Price Prediction')

# Load the stock data from the CSV file
df_stocks = pd.read_csv('pages/data.csv')
stocks = pd.Series(df_stocks.stock.values, index=df_stocks.Name).to_dict()

# Stock selection
selected_stock_name = st.selectbox('Select a stock for prediction', list(stocks.keys()))
ticker = stocks[selected_stock_name]

# Prediction period
n_years = st.slider('Years of prediction:', 1, 5)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start='2015-01-01')
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(ticker)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

# Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())

st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
