# tests/test_feature_engineering.py
import pandas as pd
import pytest

# 這是我們即將要建立的模組
from core.feature_engineering import add_technical_indicators

@pytest.fixture
def sample_ohlcv_data():
    """提供一個用於測試的 DataFrame fixture。"""
    # 需要足夠的數據來計算指標，例如 50 天的 SMA
    data = {
        'Open': range(100, 200),
        'High': range(101, 201),
        'Low': range(99, 199),
        'Close': range(100, 200),
        'Volume': range(1000, 1100)
    }
    return pd.DataFrame(data)

def test_add_technical_indicators(sample_ohlcv_data):
    # 1. 準備 (Arrange)
    data = sample_ohlcv_data

    # 2. 執行 (Act)
    featured_data = add_technical_indicators(data)

    # 3. 斷言 (Assert)
    # 斷言新的指標欄位已經被加上去了
    assert 'SMA_50' in featured_data.columns
    assert 'RSI_14' in featured_data.columns

    # 斷言 RSI 的值應該介於 0 和 100 之間 (移除 NaN 後)
    assert featured_data['RSI_14'].dropna().between(0, 100).all()

    # 斷言回傳的仍是 DataFrame
    assert isinstance(featured_data, pd.DataFrame)