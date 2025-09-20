# tests/test_backtester.py
import pytest
import pandas as pd
import numpy as np

from core.backtester import Backtester
from strategies.strategy import MovingAverageCrossoverStrategy
from data.data_handler import fetch_data

# 為了測試，我們需要一個有數據的日期範圍
TICKER = "SPY"
START_DATE = "2023-01-01"
END_DATE = "2023-03-31" # 使用較短的日期範圍以加速測試
INITIAL_CAPITAL = 10000.0

@pytest.fixture
def backtest_data():
    """提供回測所需的真實數據。"""
    return fetch_data(TICKER, START_DATE, END_DATE)

def test_backtester_returns_performance_dataframe(backtest_data):
    """測試 backtester.run() 是否回傳一個格式正確的績效 DataFrame。"""
    # 1. 準備 (Arrange)
    strategy = MovingAverageCrossoverStrategy(fast_window=10, slow_window=30)
    backtester = Backtester(initial_capital=INITIAL_CAPITAL, strategy=strategy)

    # 2. 執行 (Act)
    performance_df = backtester.run(backtest_data)

    # 3. 斷言 (Assert)
    assert isinstance(performance_df, pd.DataFrame)
    
    # 斷言必須包含這兩欄
    expected_columns = ['strategy', 'benchmark']
    assert all(col in performance_df.columns for col in expected_columns)
    
    # 斷言第一天的績效應該約等於初始資金
    assert np.isclose(performance_df['strategy'].iloc[0], INITIAL_CAPITAL)
    assert np.isclose(performance_df['benchmark'].iloc[0], INITIAL_CAPITAL)
    
    # 斷言基準（買入並持有）的最終績效計算正確
    # 基準的最終價值 = 初始資金 * (最後一天收盤價 / 第一天收盤價)
    first_close = backtest_data['Close'].iloc[0]
    last_close = backtest_data['Close'].iloc[-1]
    expected_benchmark_final = INITIAL_CAPITAL * (last_close / first_close)
    assert np.isclose(performance_df['benchmark'].iloc[-1], expected_benchmark_final)