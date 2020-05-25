import requests
from key import API_KEY1, API_KEY2, API_KEY3
import time
from _datetime import datetime
import csv
import os.path


def check_directory():
    """Checks if directory dated today exists and creates one
    if it doesnt exist
    """
    directory = "C:\\Users\\Indra\\PycharmProjects\\forex_tracker\\historical_data\\" + str(datetime.now().date())
    if not os.path.exists(directory):
        os.mkdir(directory)


def check_file(symbol):
    """Checks if file already exists in given directory
    """
    filename = 'historical_data_' + symbol.replace('/', '') + '_' + str(datetime.now().date()) + '.csv'
    directory = "C:\\Users\\Indra\\PycharmProjects\\forex_tracker\\historical_data\\" + str(
        datetime.now().date()) + "\\"
    if os.path.exists(directory + filename):
        return True


def write_csv(symbol, data):
    """Writes csv file to today's directory
    with parameters (Open, High, Low, Close, Date/Time)
    """
    check_directory()
    filename = 'historical_data_' + symbol.replace('/', '') + '_' + str(datetime.now().date()) + '.csv'
    directory = "C:\\Users\\Indra\\PycharmProjects\\forex_tracker\\historical_data\\" + str(datetime.now().date()) + "\\"
    with open((directory + filename), 'w') as csv_file:
        fieldnames = ['o', 'h', 'l', 'c', 'tm']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction='ignore')
        for a in range(len(data)):
            writer.writerow(data[a])


def pull_data():
    """Pulls data from fcsapi for historical data of 7 major pairs
    Timescale = 1hr
    """
    symbol1 = ['EUR/USD', 'USD/JPY', 'USD/CAD']
    symbol2 = ['USD/CHF', 'AUD/USD', 'GBP/USD']
    symbol3 = ['NZD/USD']
    overall_symbol = [symbol1, symbol2, symbol3]
    API_KEY_list = [API_KEY1, API_KEY2, API_KEY3]
    price_1h = {}

    for i in range(3):
        for j in range(len(overall_symbol[i])):
            # check if file already created for that day
            if check_file(overall_symbol[i][j]):
                print("File already exists...")
                continue
            else:
                response = requests.get(
                    'https://fcsapi.com/api-v2/forex/history?symbol=' + overall_symbol[i][
                        j] + '&period=1h&access_key=' +
                    API_KEY_list[i]).json()
                price_1h[overall_symbol[i][j]] = response['response']
                write_csv(overall_symbol[i][j], price_1h[overall_symbol[i][j]])
                print("Finished writing " + overall_symbol[i][j] + ".csv")
        time.sleep(60)


pull_data()
