from statsmodels.tsa.arima.model import ARIMA

def forecast_next_value(time_series):
    # Fit ARIMA model
    model = ARIMA(time_series, order=(1, 1, 1))  # Adjust order based on your data
    results = model.fit()

    # Forecast the next value
    forecast_steps = 1
    forecast = results.get_forecast(steps=forecast_steps)

    # Extract the forecasted values
    forecast_values = forecast.predicted_mean

    # Access the last forecasted value
    last_forecasted_value = forecast_values.iloc[-1]

    return last_forecasted_value