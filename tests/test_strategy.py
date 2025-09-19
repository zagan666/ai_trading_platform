# tests/test_strategy.py
import pandas as pd
import pytest

from strategies.strategy import MovingAverageCrossoverStrategy

def test_moving_average_crossover():
    # 1. 準備 (Arrange): 第三版，經過精確計算的測試數據
    # 確保在 dropna() 之後，交叉條件能被明確觸發
    data = pd.DataFrame({
        'Close': [30, 25, 20, 20, 50, 30, 20]
    })

    # 2. 執行 (Act)
    strategy = MovingAverageCrossoverStrategy(fast_window=2, slow_window=4)
    signals = strategy.generate_signals(data)

    # 3. 斷言 (Assert)
    # 經過計算，數據在 dropna 後會從索引 3 開始
    # 在索引 3: fast(20) < slow(23.75) -> HOLD
    assert signals.loc[3, 'signal'] == 'HOLD'
    
    # 在索引 4: fast(35) > slow(31.25), 且前一天 fast < slow -> BUY
    assert signals.loc[4, 'signal'] == 'BUY'
    
    # 在索引 5: fast(40) > slow(30), 但前一天 fast > slow -> HOLD
    assert signals.loc[5, 'signal'] == 'HOLD'

    # 在索引 6: fast(25) < slow(30), 且前一天 fast > slow -> SELL
    assert signals.loc[6, 'signal'] == 'SELL'