import pandas as pd
import yfinance as yf

def fetch_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start_date, end=end_date)
    df = df.rename(columns={
        'Open': 'Open',
        'High': 'High',
        'Low': 'Low',
        'Close': 'Close',
        'Volume': 'Volume',
        'Adj Close': 'Adj Close'
    })
    df['Timestamp'] = pd.to_datetime(df.index)  # 確保 Timestamp 是 datetime 格式
    df = df.reset_index(drop=True)  # 重置索引，將 Timestamp 作為普通欄位
    return df