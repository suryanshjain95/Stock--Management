import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- App Configuration ---
st.set_page_config(page_title="Comprehensive Stock Analysis", layout="wide")

# --- App Title and Sidebar ---
st.title('Comprehensive Stock Analysis Dashboard')

st.sidebar.header('User Input')
try:
    # --- User Input ---
    ticker_symbol = st.sidebar.text_input('Enter Stock Ticker', 'AAPL').upper()
    start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input('End Date', pd.to_datetime('today'))

    # --- Fetch Data ---
    ticker = yf.Ticker(ticker_symbol)
    hist_data = ticker.history(start=start_date, end=end_date)

    # Check if data is empty
    if hist_data.empty:
        st.error(f"No data found for ticker '{ticker_symbol}'. Please check the ticker symbol and date range.")
    else:
        # --- Main Page Layout ---
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Summary", "Price Chart", "Technical Analysis", "Financials", "Company Info"])

        # --- Tab 1: Summary ---
        with tab1:
            st.header(f"Key Information for {ticker_symbol}")
            info = ticker.info

            # Display company logo if available
            if 'logo_url' in info:
                st.image(info['logo_url'], width=150)

            st.subheader('Company Profile')
            st.write(f"**Name:** {info.get('longName', 'N/A')}")
            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
            st.write(f"**Website:** {info.get('website', 'N/A')}")

            st.subheader('Business Summary')
            st.write(info.get('longBusinessSummary', 'No summary available.'))

            st.subheader('Key Financial Metrics')
            # Use columns for a cleaner layout
            col1, col2, col3 = st.columns(3)
            col1.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.2f}B" if info.get('marketCap') else "N/A")
            col2.metric("P/E Ratio (Trailing)", f"{info.get('trailingPE', 0):.2f}" if info.get('trailingPE') else "N/A")
            col3.metric("Forward P/E", f"{info.get('forwardPE', 0):.2f}" if info.get('forwardPE') else "N/A")
            col1.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A")
            col2.metric("Beta", f"{info.get('beta', 0):.2f}" if info.get('beta') else "N/A")
            col3.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 0):.2f}" if info.get('fiftyTwoWeekHigh') else "N/A")


        # --- Tab 2: Price Chart ---
        with tab2:
            st.header("Price History")
            st.subheader("Candlestick Chart")
            fig_candle = go.Figure(data=[go.Candlestick(x=hist_data.index,
                                                       open=hist_data['Open'],
                                                       high=hist_data['High'],
                                                       low=hist_data['Low'],
                                                       close=hist_data['Close'])])
            fig_candle.update_layout(xaxis_rangeslider_visible=False, title=f'{ticker_symbol} Candlestick Chart')
            st.plotly_chart(fig_candle, use_container_width=True)

            st.subheader("Closing Price and Volume")
            # Create a figure with a secondary y-axis
            fig_price_vol = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                          vertical_spacing=0.05, row_heights=[0.7, 0.3])
            fig_price_vol.add_trace(go.Scatter(x=hist_data.index, y=hist_data['Close'], name='Close Price'), row=1, col=1)
            fig_price_vol.add_trace(go.Bar(x=hist_data.index, y=hist_data['Volume'], name='Volume'), row=2, col=1)
            fig_price_vol.update_layout(title_text=f"{ticker_symbol} Closing Price and Volume",
                                        yaxis1_title="Price ($)", yaxis2_title="Volume")
            st.plotly_chart(fig_price_vol, use_container_width=True)

        # --- Tab 3: Technical Analysis ---
        with tab3:
            st.header("Technical Indicators")

            st.subheader("Moving Averages (MA)")
            ma_short = st.slider('Short-term MA window', 5, 50, 20, key='ma_short')
            ma_long = st.slider('Long-term MA window', 50, 250, 50, key='ma_long')
            hist_data[f'MA{ma_short}'] = hist_data['Close'].rolling(window=ma_short).mean()
            hist_data[f'MA{ma_long}'] = hist_data['Close'].rolling(window=ma_long).mean()

            fig_ma = go.Figure()
            fig_ma.add_trace(go.Scatter(x=hist_data.index, y=hist_data['Close'], name='Close Price'))
            fig_ma.add_trace(go.Scatter(x=hist_data.index, y=hist_data[f'MA{ma_short}'], name=f'{ma_short}-Day MA'))
            fig_ma.add_trace(go.Scatter(x=hist_data.index, y=hist_data[f'MA{ma_long}'], name=f'{ma_long}-Day MA'))
            fig_ma.update_layout(title_text=f"Moving Averages for {ticker_symbol}")
            st.plotly_chart(fig_ma, use_container_width=True)

            st.subheader("Relative Strength Index (RSI)")
            delta = hist_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            hist_data['RSI'] = 100 - (100 / (1 + rs))

            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=hist_data.index, y=hist_data['RSI'], name='RSI'))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
            fig_rsi.update_layout(title_text=f"RSI for {ticker_symbol}", yaxis_title="RSI")
            st.plotly_chart(fig_rsi, use_container_width=True)

        # --- Tab 4: Financials ---
        with tab4:
            st.header(f"Financial Statements for {ticker_symbol}")
            st.subheader("Quarterly Income Statement")
            income_stmt_q = ticker.quarterly_financials
            st.dataframe(income_stmt_q)

            st.subheader("Quarterly Balance Sheet")
            balance_sheet_q = ticker.quarterly_balance_sheet
            st.dataframe(balance_sheet_q)

            st.subheader("Quarterly Cash Flow")
            cash_flow_q = ticker.quarterly_cashflow
            st.dataframe(cash_flow_q)

        # --- Tab 5: Company Info ---
        with tab5:
            st.header(f"More Info on {ticker_symbol}")
            st.subheader("Major Holders")
            st.dataframe(ticker.major_holders)

            st.subheader("Institutional Holders")
            st.dataframe(ticker.institutional_holders)

            st.subheader("Analyst Recommendations")
            st.dataframe(ticker.recommendations)

except Exception as e:
    st.error(f"An error occurred: {e}. This might be due to an invalid ticker symbol or network issues. Please try again.")
