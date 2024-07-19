import numpy as np
import pandas as pd
class trading_strategy:
    def __init__(self,strat_name,df):
        self.name=strat_name
        df['9day Sma'] = df['Close'].rolling(window=9, min_periods=1).mean()
        df['20day Sma'] = df['Close'].rolling(window=20, min_periods=1).mean()
        df['Signal'] = np.where((df['9day Sma'] > df['20day Sma']) & (df['9day Sma'].shift(1) <= df['20day Sma'].shift(1)), 1, 0)
        df['Signal'] = np.where((df['9day Sma'] < df['20day Sma']) & (df['9day Sma'].shift(1) >= df['20day Sma'].shift(1)), -1, df['Signal'])
        
    def execution(self, df,start_date, end_date):
        position = 0
        trade_open_price = 0
        df['returns'] = 0.0
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        
        for i in range(len(df)):
            if df.index[i] >= start_date and df.index[i] <= end_date:
                if df['Signal'].iloc[i] == 1:
                    if position == 0:
                        position = 1
                        trade_open_price = df['Close'].iloc[i]
                elif df['Signal'].iloc[i] == -1:
                    if position == 1:
                        position = 0
                        trade_close_price = df['Close'].iloc[i]
                        df.loc[df.index[i], 'returns'] = (trade_close_price - trade_open_price) / trade_open_price
                        trade_open_price = 0

                if position == 1 and df['Close'].iloc[i] <= trade_open_price * 0.95:
                    position = 0
                    trade_close_price = df['Close'].iloc[i]
                    df.loc[df.index[i], 'returns'] = (trade_close_price - trade_open_price) / trade_open_price
                    trade_open_price = 0
                    
        returns = df['returns'].loc[start_date:end_date].copy()
        
        return returns




# def strategy_builder(self,df):
#         df['9day Sma'] = df['Close'].rolling(window=9, min_periods=1).mean()
#         df['20day Sma'] = df['Close'].rolling(window=20, min_periods=1).mean()
#         df['Signal'] = np.where((df['9day Sma'] > df['20day Sma']) & (df['9day Sma'].shift(1) <= df['20day Sma'].shift(1)), 1, 0)
#         df['Signal'] = np.where((df['9day Sma'] < df['20day Sma']) & (df['9day Sma'].shift(1) >= df['20day Sma'].shift(1)), -1, df['Signal'])
#         return df