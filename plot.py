import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
import streamlit as st
dic={"Apple":"AAPL", "Tesla":"TSLA", "Microsoft":"MSFT","Mullen":"MULN","Bit Brother":"BETSF","Paragon":"PRGNF","Smart for Life":"SMFL","Wearable Devices":"WLDS","Kohl's Corporation":"KSS","Affymax":"AFFY","Wolfspeed":"WOLF","Beyond Meat":"BYND","American Rebel":"AREB","Entegris":"ENTG","CAVA Group":"CAVA","Amcor":"AMCR","Tapestry":"TPR","CarMax":"KMX","Pool Corporation":"POOL","Exelixis":"EXEL"}

today = date.today()

# Set the start and end date
start_date = '1990-01-01'
end_date = st.date_input("End Date", max_value="today")

#Set the ticker
if "ticker" in st.session_state:
  ticker = st.session_state.ticker
else:
  tic = st.selectbox("How would you like to be contacted?",("Apple", "Tesla", "Microsoft","Mullen","Bit Brother","Paragon","Smart for Life","Wearable Devices","Kohl's Corporation","Affymax","Wolfspeed","Beyond Meat","American Rebel","Entegris","CAVA Group","Amcor","Tapestry","CarMax","Pool Corporation","Exelixis"))
  ticker=dic[tic]

# Get the data
data = yf.download(ticker, start_date, end_date)

# Print 5 rows
data.tail()
print("\n",data)


print(data.iloc[-1,3])
print(data.iloc[-1,0])


fig, ax = plt.subplots()
ax.plot(data['Close'])
ax.set_xlabel('Year')
ax.set_ylabel('Adjusted close price')
ax.set_title('Adjusted close price data')
st.pyplot(fig)
#%matplotlib inline
# Plot adjusted close price data
#data['Close'].plot()
#plt.xlabel('Year')
#plt.ylabel('Adjusted close price')
#plt.title('Adjusted close price data')
#plt.show()
