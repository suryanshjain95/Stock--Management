import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title('Portfolio Tracker')

# Initialize session state for portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=['Ticker', 'Shares', 'Purchase Price'])

# Form to add a new stock
st.header('Add a new stock to your portfolio')
with st.form(key='add_stock_form'):
    ticker = st.text_input('Stock Ticker')
    shares = st.number_input('Number of Shares', min_value=0.01, step=0.01)
    purchase_price = st.number_input('Purchase Price', min_value=0.01, step=0.01)
    submit_button = st.form_submit_button(label='Add Stock')

    if submit_button:
        if ticker:
            new_stock = pd.DataFrame([[ticker.upper(), shares, purchase_price]], columns=['Ticker', 'Shares', 'Purchase Price'])
            st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_stock], ignore_index=True)
            st.success(f"Added {shares} shares of {ticker.upper()} to your portfolio.")
        else:
            st.error("Please enter a stock ticker.")

# Display portfolio
if not st.session_state.portfolio.empty:
    st.header('Your Portfolio')

    portfolio_df = st.session_state.portfolio.copy()

    # Get current prices
    current_prices = []
    for t in portfolio_df['Ticker']:
        stock = yf.Ticker(t)
        hist = stock.history(period='1d')
        if not hist.empty:
            current_prices.append(hist['Close'][-1])
        else:
            current_prices.append(0) # Handle cases where ticker is invalid

    portfolio_df['Current Price'] = current_prices
    portfolio_df['Current Value'] = portfolio_df['Shares'] * portfolio_df['Current Price']
    portfolio_df['Purchase Value'] = portfolio_df['Shares'] * portfolio_df['Purchase Price']
    portfolio_df['Profit/Loss'] = portfolio_df['Current Value'] - portfolio_df['Purchase Value']

    st.dataframe(portfolio_df)

    # Portfolio summary
    total_portfolio_value = portfolio_df['Current Value'].sum()
    total_purchase_value = portfolio_df['Purchase Value'].sum()
    total_profit_loss = portfolio_df['Profit/Loss'].sum()

    st.subheader('Portfolio Summary')
    st.metric('Total Portfolio Value', f"${total_portfolio_value:,.2f}", f"${total_profit_loss:,.2f}")

    # Portfolio allocation pie chart
    st.subheader('Portfolio Allocation')
    fig = px.pie(portfolio_df, values='Current Value', names='Ticker', title='Portfolio Allocation by Current Value')
    st.plotly_chart(fig)

else:
    st.info('Your portfolio is empty. Add a stock to get started.')
