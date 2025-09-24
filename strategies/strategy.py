import pandas as pd
from .base_strategy import BaseStrategy

class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, fast_window: int = 50, slow_window: int = 200):
        self.fast_window = fast_window
        self.slow_window = slow_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals_df = data.copy()
        signals_df['fast_ma'] = signals_df['Close'].rolling(window=self.fast_window).mean()
        signals_df['slow_ma'] = signals_df['Close'].rolling(window=self.slow_window).mean()
        signals_df['signal'] = 'HOLD'
        
        # 當快速均線上穿慢速均線，且前一天快速均線在慢速均線下方，觸發買入
        signals_df.loc[
            (signals_df['fast_ma'] > signals_df['slow_ma']) & 
            (signals_df['fast_ma'].shift(1) <= signals_df['slow_ma'].shift(1)), 
            'signal'
        ] = 'BUY'
        
        # 當快速均線下穿慢速均線，且前一天快速均線在慢速均線上方，觸發賣出
        signals_df.loc[
            (signals_df['fast_ma'] < signals_df['slow_ma']) & 
            (signals_df['fast_ma'].shift(1) >= signals_df['slow_ma'].shift(1)), 
            'signal'
        ] = 'SELL'
        
        return signals_df