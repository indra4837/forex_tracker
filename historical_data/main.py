from candlestick_plot import plotly_candlestick_all_currency
from pull_historical_data import pull_data


def main():
    pull_data()
    plotly_candlestick_all_currency()


if __name__ == "__main__":
    main()
