import data_pp
import trading
import numpy as np
import post_trade as pt
handler = data_pp.DataHandler(ticker='SBIN.NS', start_date='2020-01-01', end_date='2024-01-01')
handler.fetch_data()
print(handler.data.head())
print(handler.data_characteristics())
handler.performance_analysis()
strategy=trading.trading_strategy('strk',handler.data)
# strategy.strategy_builder(handler.data)
returns=strategy.execution(handler.data,'2020-06-01','2024-01-01')
print(returns)
analysis=pt.post_trade_analysis(returns)
print("Cumulative Returns:\n", analysis.cumulative_returns().tail())
print("Max Drawdown:", analysis.max_drawdown())
print("Sharpe Ratio:", analysis.sharpe_ratio())
print("Sortino Ratio:", analysis.sortino_ratio())
print("Hit Ratio:", analysis.hit_ratio())
analysis.monthly_returns_heatmap()
analysis.plot_cumulative_returns()