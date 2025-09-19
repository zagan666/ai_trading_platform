# strategies/strategy.py
import pandas as pd
import numpy as np
# 【修改點 1】從我們剛建立的 base_strategy.py 檔案中導入 BaseStrategy 類別
from .base_strategy import BaseStrategy

# 【修改點 2】在類別名稱後的括號中，加上 BaseStrategy，表示繼承關係
class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, fast_window: int, slow_window: int):
        """
        初始化均線交叉策略。

        Args:
            fast_window (int): 短天期移動平均線的窗口大小。
            slow_window (int): 長天期移動平均線的窗口大小。
        """
        self.fast_window = fast_window
        self.slow_window = slow_window

    # 這個方法完全符合 BaseStrategy 的要求，所以無需任何改動
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        根據收盤價數據產生交易信號。

        Args:
            data (pd.DataFrame): 包含 'Close' 欄位的價格數據。

        Returns:
            pd.DataFrame: 包含 'signal' 欄位的原始數據。
        """
        # --- 以下所有邏輯都維持原樣，無需任何修改 ---
        
        # 建立數據副本以避免修改原始 DataFrame
        signals_df = data.copy()

        # 計算快線和慢線
        signals_df['fast_ma'] = signals_df['Close'].rolling(window=self.fast_window).mean()
        signals_df['slow_ma'] = signals_df['Close'].rolling(window=self.slow_window).mean()
        signals_df.dropna(inplace=True) # 刪除所有包含 NaN 值的資料列

        # 初始化信號欄位，預設為持有
        signals_df['signal'] = 'HOLD'

        # 找到黃金交叉點 (快線向上穿越慢線)
        # 條件：前一天快線 <= 慢線，且今天快線 > 慢線
        buy_condition = (signals_df['fast_ma'].shift(1) <= signals_df['slow_ma'].shift(1)) & \
                        (signals_df['fast_ma'] > signals_df['slow_ma'])
        signals_df.loc[buy_condition, 'signal'] = 'BUY'

        # 找到死亡交叉點 (快線向下穿越慢線)
        # 條件：前一天快線 >= 慢線，且今天快線 < 慢線
        sell_condition = (signals_df['fast_ma'].shift(1) >= signals_df['slow_ma'].shift(1)) & \
                         (signals_df['fast_ma'] < signals_df['slow_ma'])
        signals_df.loc[sell_condition, 'signal'] = 'SELL'

        return signals_df