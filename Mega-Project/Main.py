import yfinance as yf
import pandas as pd


df = pd.read_excel("Mega_Project/NSE_symbols.xlsx")
#print(df.head())

stock_symbols = list(df['Symbol'] + ".NS")

df = pd.read_csv("Mega_Project/EQT0.csv")
l = df['Security Id'].str.replace('#', '.BO').tolist()
#print(l[:5])
stock_symbols = l+stock_symbols


import yfinance as yf
import pandas as pd

# Define the time range
start_date = "2024-01-01"
end_date = "2024-06-30"

# Placeholder for storing stock data
stock_data = []

# Fetch data for each symbol
for symbol in stock_symbols:
    try:
        stock = yf.download(symbol, start=start_date, end=end_date)
        stock['Symbol'] = symbol  # Add the symbol to the dataframe
        stock.reset_index(inplace=True)  # Reset index to move the 'Date' index to a column
        stock_data.append(stock)
        print(f"Data retrieved for {symbol}")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Combine all dataframes into one
if stock_data:
    all_stock_data = pd.concat(stock_data)
    all_stock_data.to_csv("Mega_Project/NSE_BSE_Stock_Data_2024.csv", index=False)
    print("Data successfully saved to NSE_BSE_Stock_Data_2024.csv")
else:
    print("No data to save.")
