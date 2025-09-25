import pandas as pd
import pandas_ta as ta
from core.news_sentiment import add_news_sentiment

def add_technical_indicators(data: pd.DataFrame, news_data: list = None) -> pd.DataFrame:
    df = data.copy()
    df['SMA_50'] = ta.sma(df['Close'], length=50)
    df['RSI_14'] = ta.rsi(df['Close'], length=14)
    
    # 加入新聞情緒（如果提供 news_data）
    if news_data:
        df = add_news_sentiment(df, news_data)
    
    return df