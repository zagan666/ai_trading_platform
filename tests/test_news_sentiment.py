import pytest
import pandas as pd
from core.news_sentiment import add_news_sentiment

def test_add_news_sentiment():
    # 1. 準備
    data = pd.DataFrame({
        'Close': [100, 101, 102],
        'Timestamp': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])
    })
    mock_news = [
        {'title': 'Company achieves record-breaking profits!', 'date': '2023-01-01'},  # 正向
        {'title': 'Company suffers massive financial loss', 'date': '2023-01-02'},    # 更明確的負向
        {'title': 'Market shows no significant change', 'date': '2023-01-03'}         # 中性
    ]

    # 2. 執行
    result = add_news_sentiment(data, mock_news)

    # 3. 斷言
    assert 'sentiment' in result.columns
    assert len(result) == len(data)
    assert result['sentiment'].iloc[0] > 0  # 正向新聞，分數應 > 0
    assert result['sentiment'].iloc[1] < 0  # 負向新聞，分數應 < 0
    assert result['sentiment'].iloc[2] == 0  # 中性新聞，分數應 = 0