import numpy as np
import pandas as pd
import openpyxl


class trading_strategy:
    
    def __init__(self,strat_name):
        self.name=strat_name
        
    def strategy_builder(self,df):
        df['9day Sma'] = df['Close'].rolling(window=9, min_periods=1).mean()
        df['20day Sma'] = df['Close'].rolling(window=20, min_periods=1).mean()
        df['Signal'] = np.where((df['9day Sma'] > df['20day Sma']) & (df['9day Sma'].shift(1) <= df['20day Sma'].shift(1)), 1, 
                                np.where((df['9day Sma'] < df['20day Sma']) & (df['9day Sma'].shift(1) >= df['20day Sma'].shift(1)), -1, 0))
        return df
    
    def execution(self, df, ticker, start_date, end_date):
        
        position=0
        position = 0
        trade_open_price = 0
        df['returns'] = 0.0
    
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        
        mask = (df.index >= start_date) & (df.index <= end_date)
        df_filtered = df.loc[mask]
    
    
        for i in range(len(df_filtered)):

                if df_filtered['Signal'].iloc[i] == 1:
                    if position == 0:
                        position = 1
                        trade_open_price = df_filtered['Close'].iloc[i]
                        
                elif df_filtered['Signal'].iloc[i] == -1:
                    if position == 1:
                        position = 0
                        trade_close_price = df_filtered['Close'].iloc[i]
                        df_filtered.loc[df_filtered.index[i], 'returns'] = (trade_close_price - trade_open_price) / trade_open_price
                        trade_open_price = 0

                if position == 1 and df_filtered['Close'].iloc[i] <= trade_open_price * 0.95:
                    position = 0
                    trade_close_price = df_filtered['Close'].iloc[i]
                    df_filtered.loc[df_filtered.index[i], 'returns'] = (trade_close_price - trade_open_price) / trade_open_price
                    trade_open_price = 0
                    
        returns = df_filtered['returns'].loc[start_date:end_date].copy()
        
        return returns




