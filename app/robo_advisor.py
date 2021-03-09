import os
from dotenv import load_dotenv
import requests 
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator
import time
#load environmental variables
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
os.getcwd()

# Make a get request to the api and return the records
def make_request(stock): 
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={API_KEY}"
    response = requests.get(request_url)
    if float(response.status_code) != 200:
        print ("There seems to be an error! Please try again later")
        return
    parsed_response = json.loads(response.text)
    if len(parsed_response) > 1:
        records = parse_data(parsed_response)
        returned_output(parsed_response, records)
        #plot_graph(records)
        return (stock, records)
    else:
        print("The symbol " + stock +" does not seem to be a valid stock")
        return -1

# Helper function to convert the string date into a more accessible format of datetime
def convert_date(str_date):
    str_date = str_date.split(" ")[0]
    format_string = "%Y-%m-%d"
    date_obj = datetime.datetime.strptime(str_date, format_string)
    return date_obj.strftime("Latest Data From %B %d, %Y")

# Helper function to convert float dollar amount to string format with dollar sign
def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

# Helper function which presents the printed output to the user and performs necessary calculations   
def returned_output(parsed_response, records):
    output = ''
    now = datetime.datetime.now()
    symbol = parsed_response["Meta Data"]["2. Symbol"]
    current_date = now.strftime("Run at %H:%M:%S on %B %d, %Y")
    last_refreshed = convert_date(parsed_response["Meta Data"]["3. Last Refreshed"])
    latest_closing_price = to_usd(float(records[0]["close"]))
    all_high = [x['high'] for x in records[:100]]
    all_low = [x['low'] for x in records[:100]]
    recent_high = max(all_high)
    recent_low = min(all_low)
    should_buy = float(records[0]["close"]) <=  (recent_low + 0.2 * recent_low)
    
    output += "Symbol: " + symbol + '\n'
    output += current_date + '\n'
    output += last_refreshed + '\n'
    output += "Latest closing price is: " + latest_closing_price +'\n'
    output += "Recent high is: " + to_usd(recent_high) + '\n'
    output += "Recent low is: " + to_usd(recent_low) + '\n'
    if should_buy: 
        output += f"Reccomendation: Buy {symbol} as the closing price {latest_closing_price}, is not greater than {to_usd(recent_low + 0.2 * recent_low)} and is within 20% of the recent low of {to_usd(recent_low)}"
    else:
        output += f"Reccomendation: Do Not Buy {symbol} as the closing price {latest_closing_price}, is greater than {to_usd(recent_low + 0.2 * recent_low)} and is not within 20% of the recent low of {to_usd(recent_low)}"

    df = pd.DataFrame(records)
    df.to_csv(os.path.join(os.path.dirname(__file__), "..", "data/" + symbol), index = False)
    print(output)
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print('\n')
    

# Helper function to plot a comparison graph/ individual graph of a stock.  
def plot_graph(records): 

    for r in records:
        y_val = [x['close'] for x in r[1]]
        x_val = [x['date'] for x in r[1]]
        plt.xlabel('Date')
        plt.ylabel('Daily Closing Price')
        plt.gcf().autofmt_xdate()
        ticks = range(len(x_val))
        labels =  x_val[::-1]
        y_val = y_val[::-1]
        n = len(ticks) // 10  
        plt.xticks(ticks[::n], labels[::n])
        plt.plot(x_val, y_val, label = r[0])
    
    plt.legend()
    plt.show()


# Helper function to parse the data into a more readable format, to make calculations and indexing easier. 
def parse_data(parsed_response):
    records = []
    for date, daily_data in parsed_response["Time Series (Daily)"].items():
        record = {
            "date": date,
            "open": float(daily_data["1. open"]),
            "high": float(daily_data["2. high"]),
            "low": float(daily_data["3. low"]),
            "close": float(daily_data["4. close"]),
            "volume": int(daily_data["5. volume"]),
        }
        records.append(record)


    return records


# Main function which actually runs the code. 
def main():
    print("input a stock symbol that you would like to get information about or type 'DONE' to exit!")
    print("If you would like to compare multiple stocks, you can enter multiple symbols as a comma separated list.")
    while True:
        stock = input("Please input the symbol(s) of the stock(s) you would like to get information about or type DONE: ")
        if stock == "DONE":
            return
        all_stocks = stock.split(',')
        print("fetching data for stocks", all_stocks)
        stock_records = []
        for stk in all_stocks:
            if len(stk) >= 1 and len(stk) <= 5 and stk.isalpha():
                r = make_request(stk.upper())
                if r != -1: 
                    stock_records.append(r)
                # Add some delay between requests, so that no time out requests occour. 
                time.sleep(5)
            else:
                print("The symbol " + stk + " seems to be incorrect, so I will ignore that from your input!")
        
        if len(stock_records) > 0:
            plot_graph(stock_records)

main()