# tests/test_data_handler.py

import pytest
import pandas as pd

# 我們預期未來在 data/data_handler.py 檔案中會有一個名為 fetch_data 的函式
from data.data_handler import fetch_data

def test_fetch_data_returns_dataframe():
    """
    測試 fetch_data 函式是否能成功返回一個非空的 Pandas DataFrame。
    """
    # 1. 準備 (Arrange)
    ticker = "SPY"  # 使用 SPY (S&P 500 ETF) 作為測試標的
    start_date = "2023-01-01"
    end_date = "2023-01-31"

    # 2. 執行 (Act)
    # 我們嘗試呼叫那個還不存在的函式
    data = fetch_data(ticker, start_date, end_date)

    # 3. 斷言 (Assert)
    # 斷言返回的必須是 Pandas DataFrame
    assert isinstance(data, pd.DataFrame)
    
    # 斷言 DataFrame 不能是空的
    assert not data.empty
    
    # 斷言 DataFrame 必須包含我們需要的欄位
    expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    assert all(col in data.columns for col in expected_columns)