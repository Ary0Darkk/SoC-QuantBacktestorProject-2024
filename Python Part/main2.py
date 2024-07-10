import data_pp
import trading
handler = data_pp.DataHandler(ticker='SBIN.NS', start_date='2020-01-01', end_date='2024-01-01')
handler.fetch_data()
print(handler.data.head())
print(handler.data_characteristics())
handler.performance_analysis()
strategy=trading.trading_strategy('strk')
strategy.strategy_builder(handler.data)
returns=strategy.execution(handler.data,'RELIANCE.NS','2020-06-01','2024-01-01')
print(returns)
print(handler.data)
total_return=(1+returns).cumprod()
print(total_return)