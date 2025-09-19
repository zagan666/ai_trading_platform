# core/feature_engineering.py

import pandas as pd
import pandas_ta as ta

def add_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    在 OHLCV DataFrame 上計算並添加常用的技術指標作為特徵。

    Args:
        data (pd.DataFrame): 必須包含 'Open', 'High', 'Low', 'Close', 'Volume' 欄位。

    Returns:
        pd.DataFrame: 增加了技術指標欄位的新 DataFrame。
    """
    # 複製一份數據以避免修改原始傳入的 DataFrame
    df = data.copy()

    # 使用 pandas_ta 來計算並添加指標。
    # .ta.sma() 會計算簡單移動平均線，append=True 會自動將結果 ('SMA_50') 加入 df。
    df.ta.sma(length=50, append=True)

    # .ta.rsi() 會計算相對強弱指數，append=True 會自動將結果 ('RSI_14') 加入 df。
    df.ta.rsi(length=14, append=True)

    # 未來可以輕鬆地在此處添加更多指標，例如：
    # df.ta.bbands(length=20, append=True) # 布林通道
    # df.ta.macd(append=True) # MACD

    # 刪除因為計算指標而產生的 NaN 值
    df.dropna(inplace=True)

    return df