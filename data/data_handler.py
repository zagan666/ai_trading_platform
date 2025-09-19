# data/data_handler.py

import pandas as pd
import yfinance as yf

def fetch_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    從 Yahoo Finance 獲取指定股票代碼的歷史數據。

    Args:
        ticker (str): 股票代碼, 例如 "SPY".
        start_date (str): 開始日期, 格式 "YYYY-MM-DD".
        end_date (str): 結束日期, 格式 "YYYY-MM-DD".

    Returns:
        pd.DataFrame: 包含 OHLCV 數據的 DataFrame。
    """
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    return data