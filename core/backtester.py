# core/backtester.py

import pandas as pd
# 為了做型別提示(Type Hinting)，導入我們的策略類別
from strategies.strategy import MovingAverageCrossoverStrategy 

class Backtester:
    """
    執行交易策略回測的核心引擎。
    """

    # __init__ 方法，正確縮排在 class 之下
    def __init__(self, initial_capital: float, strategy: MovingAverageCrossoverStrategy):
        """
        初始化回測器。

        Args:
            initial_capital (float): 初始資金。
            strategy: 一個策略物件，該物件必須有 generate_signals 方法。
        """
        self.initial_capital = initial_capital
        self.strategy = strategy
        
        # 初始化帳戶狀態
        self.cash = initial_capital
        self.position = 0.0
        self.portfolio_history = []

    # run 方法，也正確縮排在 class 之下
    def run(self, data: pd.DataFrame) -> dict:
        """
        執行回測並返回績效結果。

        Args:
            data (pd.DataFrame): 包含價格數據的 DataFrame，至少需要 'Close' 欄位。

        Returns:
            dict: 一個包含回測績效指標的字典。
        """
        # 1. 根據傳入的數據，讓策略物件產生交易信號
        signals_df = self.strategy.generate_signals(data)

        # 2. 模擬逐日交易
        for index, row in signals_df.iterrows():
            # 【關鍵修正】使用 .item() 從 Pandas Series 中提取純數值和字串
            current_price = row['Close']
            signal = row['signal']
            
            # 使用新的 signal 變數進行判斷
            if signal == 'BUY' and self.cash > 0:
                shares_to_buy = self.cash / current_price
                self.position += shares_to_buy
                self.cash = 0.0

            elif signal == 'SELL' and self.position > 0:
                self.cash += self.position * current_price
                self.position = 0.0
            
            # 計算當日總資產淨值並記錄
            current_portfolio_value = self.cash + (self.position * current_price)
            self.portfolio_history.append(current_portfolio_value)

        # 3. 準備回測結果
        if not self.portfolio_history:
            final_portfolio_value = self.initial_capital
        else:
            final_portfolio_value = self.portfolio_history[-1]

        result = {
            'final_portfolio_value': final_portfolio_value,
            # 未來可以增加更多績效指標
        }
        
        return result