import pandas as pd
from datetime import timedelta
import time
import warnings
import configparser
from iqoptionapi.stable_api import IQ_Option
from src.backtest import backtest
from src.forecast_arima import forecast_next_value

from src.connection import login

# To ignore all warnings
warnings.filterwarnings("ignore")

# Function to fetch historical stock data from Yahoo Finance
def get_stock_data(iq):
    goal = "EURUSD"
    expiration_remaning_minutes = 1
    current = iq.get_candles(ACTIVES=goal, interval=expiration_remaning_minutes*60, count=100, endtime=time.time())
    data = pd.DataFrame(current)
    # data = data.rename(columns={'open': 'Open', 'max': 'High', 'min': 'Low', 'close': 'Close', 'volume': 'Volume'})
    data.drop_duplicates(inplace=True)
    # data = data.iloc[:-1]
    return data.iloc[:-1]['close']

def main():
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    user_info = config['USERINFO']
    
    try:
        iq = login(email=user_info['email'], password=user_info['password'])
    except Exception as e:
        print("Error connection to iq: ", e)
        exit(1)
        
    if config['MODE']['backtest'] == "enable":
        stock_data = get_stock_data(iq)
        backtest(stock_data)
        print(f'------------------------------------------')
    
    # Fetch historical stock data
    stock_data = get_stock_data(iq)

    # Forecast the next value
    next_value = forecast_next_value(stock_data)

    # Determine if the next value is higher or lower than the last observed value
    last_observed_value = stock_data.iloc[-1]
    if next_value > last_observed_value:
        trend = 'higher'
    elif next_value < last_observed_value:
        trend = 'lower'
    else:
        trend = 'unchanged'

    # Print the forecasted and observed values along with the trend
    print(f'Last Observed Value: {last_observed_value}')
    print(f'Forecasted Next Value: {next_value}')
    print(f'Trend: {trend}')
    
if __name__ == '__main__':
    main()