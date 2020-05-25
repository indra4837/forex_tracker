import plotly.graph_objs as go
from _datetime import datetime
import pandas as pd
import plotly.io as pio
import mplfinance as mpf
from plotly.subplots import make_subplots


def process_data_plotly():
    """Reads .csv file into pandas dataframe and processes data
    for plotly
    """
    df = {}
    symbols = ['EUR/USD', 'USD/JPY', 'USD/CHF', 'USD/CAD', 'AUD/USD', 'GBP/USD', 'NZD/USD']

    for i in range(len(symbols)):
        filename = ('historical_data_' + symbols[i].replace('/', '') + '_' + str(datetime.now().date()) + '.csv')
        filepath = 'C:\\Users\\Indra\\PycharmProjects\\forex_tracker\\historical_data\\' + str(datetime.now().date())
        header = ['Open', 'High', 'Low', 'Close', 'Date']
        temp = pd.read_csv((filepath + '\\' + filename), names=header)
        temp = temp[['Date', 'Open', 'High', 'Low', 'Close']]  # rearrange column to fit mplfinance
        df[symbols[i]] = temp

    return df


def process_data_mpl():
    """Reads .csv file into pandas dataframe and processes data
    for mplfinance
    """
    df = process_data_plotly()

    for key, value in df.items():
        value['Date'] = pd.to_datetime(value['Date'], errors='coerce')
        value = value.set_index('Date')
        # df.index = pd.to_datetime(df.index)
        # df.index.name = 'Date'
        print(value)

    return df


def ema():
    """Calculates exponential moving average using
    pandas dataframe ewm method
    """
    overall_ema_dict = {}
    df_dict = process_data_plotly()
    #key: Currency, value: dataframe
    for key, value in df_dict.items():
        value = value.drop(columns=['Open', 'High', 'Low'])
        close = value.loc[:, ['Close']]
        date = value.loc[:, 'Date']
        ema8 = close.ewm(span=8, adjust=False).mean()
        ema8.insert(loc=0, value=date, column='Date')
        ema13 = close.ewm(span=13, adjust=False).mean()
        ema13.insert(loc=0, value=date, column='Date')
        ema21 = close.ewm(span=21, adjust=False).mean()
        ema21.insert(loc=0, value=date, column='Date')
        overall_ema_dict[key] = list(({'ema8': ema8}, {'ema13': ema13}, {'ema21': ema21}))

    return overall_ema_dict


def plotly_candlestick_single_currency(symbol, df_candle, ema_list):
    """Uses plotly library to plot candlestick for each currency
    """
    pio.renderers.default = 'browser'

    data = [go.Candlestick(x=df_candle['Date'],
                           open=df_candle['Open'],
                           high=df_candle['High'],
                           low=df_candle['Low'],
                           close=df_candle['Close']),
            go.Scatter(x=(ema_list[0]['ema8']).loc[:, 'Date'],
                       y=(ema_list[0]['ema8']).loc[:, 'Close'],
                       line=dict(color='orange', width=1),
                       name='EMA8'),
            go.Scatter(x=(ema_list[1]['ema13']).loc[:, 'Date'],
                       y=(ema_list[1]['ema13']).loc[:, 'Close'],
                       line=dict(color='red', width=1),
                       name='EMA13'),
            go.Scatter(x=(ema_list[2]['ema21']).loc[:, 'Date'],
                       y=(ema_list[2]['ema21']).loc[:, 'Close'],
                       line=dict(color='blue', width=1),
                       name='EMA21')]

    figSignal = go.Figure(data=data)
    rangebreaks = [dict(enabled=True)]
    figSignal.update_layout(title=symbol)
    figSignal.update_xaxes(rangebreaks=rangebreaks)

    figSignal.show()


def plotly_candlestick_all_currency():
    """Uses plotly to plot all currency
    via plotly_candlestick_single_currency function
    """
    overall_ema_dict = ema()
    df = process_data_plotly()
    for key, value in df.items():
        plotly_candlestick_single_currency(key, value, overall_ema_dict[key])


def mpl_candlestick_single_currency(data):
    """Uses mplfinance to plot single currency
    """
    mpf.plot(data, type='candle')


def mpl_candlestick_all_currency():
    """Uses mplfinance to plot all currency
    via mpl_candlestick_single_currency function
    """
    df = process_data_mpl()
    for key, value in df.items():
        mpl_candlestick_single_currency(value)


plotly_candlestick_all_currency()
