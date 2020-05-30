from historical_data.candlestick_plot import *


def get_extreme_value_candle(df) -> tuple:
    """Returns (lowest, highest) tuple for each time-entry in candle
    """
    return df.values.max(), df.values.min()


def get_extreme_value_ema(ema8, ema13, ema21) -> tuple:
    """Returns (lowest, highest) tuple for each time-entry in EMA list
    """
    return max(ema8, ema13, ema21), min(ema8, ema13, ema21)


def candle_pos_wrt_ema() -> str:
    """Check if candles above/below EMA line
    Above: Pending long
    Below: Pending short
    Strategy: If ema != lowest-highest, check previous 4 values for same characteristic
    """
    ema_data = ema()
    candle_data = process_data_plotly()
    # categories: top, hit, bottom (w.r.t ema line)
    positions_candle = {'EUR/USD': [], 'AUD/USD': [], 'GBP/USD': [], 'NZD/USD': [], 'USD/CAD': [], 'USD/CHF': [],
                        'USD/JPY': []}

    for k, v in candle_data.items():

        v = v.drop(columns=['Date'])  # can reference to date using index
        ema8 = ema_data[k][0]['ema8'].drop(columns='Date')
        ema13 = ema_data[k][1]['ema13'].drop(columns='Date')
        ema21 = ema_data[k][2]['ema21'].drop(columns='Date')

        for j in range(len(v)):
            temp_candle = v.iloc[j]
            ema8_value = ema8.iloc[j]
            ema13_value = ema13.iloc[j]
            ema21_value = ema21.iloc[j]
            (max_candle, min_candle) = get_extreme_value_candle(temp_candle)
            (max_ema, min_ema) = get_extreme_value_ema(ema8_value.item(), ema13_value.item(), ema21_value.item())
            if max_candle < min_ema:
                positions_candle[k].append((j, 'Bottom'))
            elif min_candle > max_ema:
                positions_candle[k].append((j, 'Top'))
            else:
                positions_candle[k].append((j, 'Hit'))

    return positions_candle


def checking_setup():
    trailing_checks = 5  # num of prev. positions of candle to check
    setup_confirmed = {'EUR/USD': [], 'AUD/USD': [], 'GBP/USD': [], 'NZD/USD': [], 'USD/CAD': [], 'USD/CHF': [],
                       'USD/JPY': []}
    positions = candle_pos_wrt_ema()

    for k, v in positions.items():
        # start index from 3 since we are checking prev 3 (error handling)
        for i in range(trailing_checks, len(v)):
            if positions[k][i][1] == 'Hit':
                if sum(1 for j in range(i - trailing_checks, i)
                       if positions[k][j][1] == 'Bottom') == trailing_checks:
                    setup_confirmed[k].append((i, 'Short'))
                elif sum(1 for j in range(i - trailing_checks, i)
                         if positions[k][j][1] == 'Top') == trailing_checks:
                    setup_confirmed[k].append((i, 'Long'))

    #   TODO: code decomposition -> check_trailing_positions (function)
    # print(setup_confirmed)
    return setup_confirmed


def stoploss_takeprofit():
    """Calculates stop-loss and take-profit for each trade
    """

    trailing_checks = 5
    risk = 1.5
    candle_data = process_data_plotly()
    for k, v in candle_data.items():
        candle_data[k].insert(5, 'Stop Loss', 0)
        candle_data[k].insert(6, 'Take Profit', 0)
        candle_data[k].insert(7, 'Type', 0)

    setup = checking_setup()

    # remove all columns except high and low
    for k, v in candle_data.items():
        temp = v.drop(columns=['Date'])
        for i in range(7):
            candle_data[k] = temp

    for k, v in setup.items():
        for i in range(len(v)):
            if v[i][1] == 'Short':
                index = v[i][0]
                candle_data[k].loc[index, 'Type'] = 'Short'
                sl = max(candle_data[k].iloc[j].values.max() for j in range(index - 4, index))
                candle_data[k].loc[index, 'Stop Loss'] = float(sl)
                tp = candle_data[k].loc[index, 'Close'] - risk * (sl - candle_data[k].loc[index, 'Close'])
                candle_data[k].loc[index, 'Take Profit'] = float(tp)

            elif v[i][1] == 'Long':
                index = v[i][0]
                candle_data[k].loc[index, 'Type'] = 'Long'
                sl = min(candle_data[k].iloc[j]['Low'] for j in range(index - 4, index))
                candle_data[k].loc[index, 'Stop Loss'] = float(sl)
                tp = candle_data[k].loc[index, 'Close'] + risk * (sl - candle_data[k].loc[index, 'Close'])
                candle_data[k].loc[index, 'Take Profit'] = float(tp)

    # candle_data['EUR/USD'].to_csv(r'C:\\Users\\Indra\\PycharmProjects\\forex_tracker\\Backtesting\\test.csv',
    # index=False)

    return candle_data




# candle_pos_wrt_ema()
# checking_setup()
# print(process_data_plotly())
stoploss_takeprofit()
