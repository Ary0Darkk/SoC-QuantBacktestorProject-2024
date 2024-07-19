import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class DataHandler:
    def __init__(self,ticker, start_date, end_date):
        self.ticker=ticker
        self.start_date=start_date
        self.end_date=end_date
    
    def fetch_data(self):
        self.data=self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return self.data
    def download_historical_data(self,timeframe='1d'):
        df=yf.download(self.ticker,start=self.start_date,end=self.end_date,interval=timeframe)
        return df
    def data_characteristics(self):
        summary = self.data.describe().T
        summary['median'] = self.data.median()
        summary['mode'] = self.data.mode().iloc[0]
        return summary
    def missing_value_handler(self):
        self.data.dropna()
        return self.data
    def performance_analysis(self):
        nifty_data = yf.download('^NSEI', start=self.start_date, end=self.end_date)
        log_returns=np.log(self.data['Adj Close']/self.data['Adj Close'].shift(1))
        cum_log_returns=log_returns.cumsum()
        nifty_log_returns=np.log(nifty_data['Adj Close']/nifty_data['Adj Close'].shift(1))
        cum_nif_returns=nifty_log_returns.cumsum()
        plt.figure(figsize=(12, 6))
        plt.plot(cum_log_returns, label=f'{self.ticker} Cumulative Returns')
        plt.plot(cum_nif_returns, label='Nifty Cumulative Returns')
        plt.title(f'Performance of {self.ticker} vs Nifty')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.show()