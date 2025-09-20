# core/backtester.py
import pandas as pd
from strategies.base_strategy import BaseStrategy

class Backtester:
    def __init__(self, initial_capital: float, strategy: BaseStrategy):
        self.initial_capital = initial_capital
        self.strategy = strategy
        self.cash = initial_capital
        self.position = 0.0
        self.portfolio_history = []

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        performance_df = pd.DataFrame(index=data.index)

        first_close = data['Close'].iloc[0]
        performance_df['benchmark'] = self.initial_capital * (data['Close'] / first_close)

        signals_df = self.strategy.generate_signals(data)
        
        self.cash = self.initial_capital
        self.position = 0.0
        self.portfolio_history = []
        
        for index, row in signals_df.iterrows():
            current_price = row['Close']
            signal = row['signal']
            
            if signal == 'BUY' and self.cash > 0:
                shares_to_buy = self.cash / current_price
                self.position += shares_to_buy
                self.cash = 0.0
            elif signal == 'SELL' and self.position > 0:
                self.cash += self.position * current_price
                self.position = 0.0
            
            current_portfolio_value = self.cash + (self.position * current_price)
            self.portfolio_history.append(current_portfolio_value)

        strategy_performance = pd.Series(self.portfolio_history, index=signals_df.index)
        performance_df['strategy'] = strategy_performance
        
        # 【關鍵修正】使用賦值的方式取代 inplace=True
        performance_df['strategy'] = performance_df['strategy'].fillna(self.initial_capital)
        
        return performance_df