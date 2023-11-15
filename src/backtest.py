from src.forecast_arima import forecast_next_value
import configparser

def backtest(stock_data):
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Perform backtest
    correct_trend_count = 0

    pos_to = 90
    
    size = int(config['ORDER']['POS_SIZE'])
    position_size = size
    balance = int(config['ORDER']['BALANCE'])

    for i in range(pos_to, len(stock_data)):
        # Slice the time series up to the current index for forecasting
        current_series = stock_data.iloc[:i]

        # Forecast the next value
        next_value = forecast_next_value(current_series)

        # Determine if the next value is higher or lower than the last observed value
        last_observed_value = current_series.iloc[-1]
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

        # Check if the forecasted trend is correct
        if stock_data.iloc[i] > last_observed_value and trend == 'higher':
            correct_trend_count += 1
            balance = balance + (0.85 * position_size)
            position_size = size
            print(f'ac: true')
            print(f'Balance: {balance}')
        elif stock_data.iloc[i] < last_observed_value and trend == 'lower':
            correct_trend_count += 1
            balance = balance + (0.85 * position_size)
            position_size = size
            print(f'ac: true')
            print(f'Balance: {balance}')
        elif trend == 'unchanged':
            pass
        else:
            balance = balance - position_size
            position_size *= 2
            print(f'ac: false')
            print(f'Balance: {balance}')
            print(f'next position_size: {position_size}')
        
        print(f'------------------------------------------')

    # Calculate accuracy
    total_forecasts = len(stock_data) - 1 - pos_to
    accuracy = correct_trend_count / total_forecasts

    # Print the backtest results
    print(f'Number of Correct Trends: {correct_trend_count}')
    print(f'Total Number of Forecasts: {total_forecasts}')
    print(f'Accuracy: {accuracy * 100:.2f}%')
    print(f'Balance: {balance}')
