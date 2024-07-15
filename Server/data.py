import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import numpy as np
import os



class DataHandler:
    
    def __init__(self, ticker, start_date, end_date):
        
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def fetch_data(self, timeframe='1d'):
        
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date, interval=timeframe)
        
        return self.data

    def data_characteristics(self):
        if self.data is None:
            self.data = self.fetch_data()
            
        summary = self.data.describe().T
        summary['median'] = self.data.median()
        
        if not self.data.empty:
            summary['mode'] = self.data.mode().iloc[0]
        else:
            summary['mode'] = None 
             
        return summary.to_dict()

    def missing_value_handler(self):
        if self.data is None:
            self.data = self.fetch_data()
        self.data = self.data.dropna()
        return {'message': 'Missing values dropped'}

    def performance_analysis(self):
        if self.data is None:
            self.data = self.fetch_data()
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
        
        file_name = f'{self.ticker}_cumulative_returns.png'

        savein = os.path.join('../client/src/static', file_name )
        plot_path = f"../static/{file_name}"
        plt.savefig(savein)
        plt.close()
        print(plot_path, file_name)
        return plot_path
