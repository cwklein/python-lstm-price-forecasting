import numpy as np
import pandas as pd
import tensorflow as tf
import yfinance as yf
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
pd.options.mode.chained_assignment = None
tf.random.set_seed(0)

def lstmModelUpdate(company):
    # Download data
    df_main = yf.download(tickers=[company], period='2y')
    y_values = df_main['Close'].fillna(method='ffill')
    y_values = y_values.values.reshape(-1, 1)

    # Scale the data to be between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(y_values)
    y_values = scaler.transform(y_values)

    # Generate input(lookback) and output(forecast) sequences
    n_lookback = 90  # length of input (lookback period)
    n_forecast = 30  # length of output (forecast period)

    x_array = []
    y_array = []

    for i in range(n_lookback, len(y_values) - n_forecast + 1):
        x_array.append(y_values[i - n_lookback: i])
        y_array.append(y_values[i: i + n_forecast])

    x_array = np.array(x_array)
    y_array = np.array(y_array)

    # Create and train model
    model = Sequential()
    model.add(LSTM(units=75, return_sequences=True, input_shape=(n_lookback, 1)))
    model.add(LSTM(units=75))
    model.add(Dense(n_forecast))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_array, y_array, epochs=7, batch_size=2, verbose=1)

    # Generate forecasts based on trained model
    x_forecast = y_values[- n_lookback:]  # last available input sequence
    x_forecast = x_forecast.reshape(1, n_lookback, 1)

    y_forecast = model.predict(x_forecast).reshape(-1, 1)
    y_forecast = scaler.inverse_transform(y_forecast)

    # Split results into past and future dataframes with proper indices
    df_past = df_main[['Close']].reset_index()
    df_past.rename(columns={'index': 'Date', 'Close': 'Actual'}, inplace=True)
    df_past['Date'] = pd.to_datetime(df_past['Date'])
    df_past['Forecast'] = np.nan
    df_past['Forecast'].iloc[-1] = df_past['Actual'].iloc[-1] #Just closes gap in plot, doesn't affect values

    df_future = pd.DataFrame(columns=['Date', 'Actual', 'Forecast'])
    df_future['Date'] = pd.date_range(start=df_past['Date'].iloc[-1], periods=n_forecast)
    df_future['Forecast'] = y_forecast.flatten()
    df_future['Actual'] = np.nan

    results = df_past.append(df_future).set_index('Date')

    # Prepare the figure
    fig = results.plot(figsize=(11.83,5.01), title=f'{company} - 2 Year Performance').get_figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.1)

    # Save figure as png for web app
    fig.savefig(f'/home/ColbyKid/capstoneProject/static/{company}_lstm_final', format='png')

    # Retrieve relevant datapoints for web app
    last_date_full = df_main.index[-1]
    last_date = last_date_full.strftime('%m/%d/%Y')
    last_close_valid = str("%.2f" % df_main['Close'].iloc[-1])
    last_close_predicted = str("%.2f" % pd.DataFrame(y_forecast)[0][0])

    # Put relevant datapoints into df to export to csv
    out_values = {'Values' : [last_date, last_close_valid, last_close_predicted]}
    df_out = pd.DataFrame(out_values)

    # Export df's to csv
    output_name = f'/home/ColbyKid/capstoneProject/static/{company}_info.csv'
    df_out.to_csv(output_name)

    data_name = f'/home/ColbyKid/capstoneProject/static/{company}_data_full.csv'
    df_main.to_csv(data_name)

def lstmMainPage():
    # Download data & rename columns
    df_AAPL = pd.read_csv('/home/ColbyKid/capstoneProject/static/AAPL_data_full.csv', usecols = ['Date', 'Close'])
    df_AAPL.rename(columns = {'Close':'AAPL'}, inplace = True)

    df_AMZN = pd.read_csv('/home/ColbyKid/capstoneProject/static/AMZN_data_full.csv', usecols = ['Date', 'Close'])
    df_AMZN.rename(columns = {'Close':'AMZN'}, inplace = True)

    df_MSFT = pd.read_csv('/home/ColbyKid/capstoneProject/static/MSFT_data_full.csv', usecols = ['Date', 'Close'])
    df_MSFT.rename(columns = {'Close':'MSFT'}, inplace = True)

    # Merge df's into single df
    df_temp = df_AAPL.merge(df_AMZN, how='inner', on='Date')
    df_total = df_temp.merge(df_MSFT, how='inner', on='Date')

    # Standardize data for graphing
    df_total['Date'] = pd.to_datetime(df_total['Date'])
    df_total = df_total.set_index('Date')

    # Prepare the figure
    fig = df_total.plot(figsize=(11.83,5.01), title='Sample Companies - 2 Year Performance').get_figure()
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.1)

    # Save figure as png for web app
    fig.savefig('/home/ColbyKid/capstoneProject/static/all_lstm', format='png')

# Run all functions to generate graphs and data points
lstmModelUpdate('AAPL')
lstmModelUpdate('AMZN')
lstmModelUpdate('MSFT')
lstmMainPage()
print('Done')