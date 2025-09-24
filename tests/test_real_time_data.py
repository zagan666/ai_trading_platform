# tests/test_real_time_data.py
import pytest
import pandas as pd
from data.real_time_data import get_real_time_data

@pytest.mark.asyncio
async def test_get_real_time_data():
    # 1. 準備
    exchange = "binance"
    symbol = "BTC/USDT"
    limit = 1  # 只取最新一筆

    # 2. 執行
    data = await get_real_time_data(exchange, symbol, limit)

    # 3. 斷言
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    expected_columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    assert all(col in data.columns for col in expected_columns)