# tests/test_backtester.py
import pytest

# 這是我們要測試的核心模組
from core.backtester import Backtester
# 這是我們的策略模組
from strategies.strategy import MovingAverageCrossoverStrategy
# 這是我們的數據模組
from data.data_handler import fetch_data

def test_backtester_run():
    # 1. 準備 (Arrange)
    # 準備回測所需的所有元件
    ticker = "SPY"
    start_date = "2022-01-01"
    end_date = "2022-12-31"
    initial_capital = 10000.0

    # 獲取真實數據
    data = fetch_data(ticker, start_date, end_date)

    # 建立策略物件
    strategy = MovingAverageCrossoverStrategy(fast_window=50, slow_window=200)

    # 2. 執行 (Act)
    # 建立回測器物件並執行回測
    backtester = Backtester(initial_capital=initial_capital, strategy=strategy)
    result = backtester.run(data)

    # 3. 斷言 (Assert)
    # 簡單地斷言回測結果是一個字典，且包含了關鍵績效指標
    assert isinstance(result, dict)

    # 斷言最終資產淨值存在且是一個浮點數
    assert 'final_portfolio_value' in result
    assert isinstance(result['final_portfolio_value'], float)

    # 斷言最終資產不應為零（對於一整年的 SPY 數據，這幾乎不可能）
    assert result['final_portfolio_value'] > 0