import pytest
import pandas as pd
from core.feature_engineering import add_technical_indicators

def test_add_technical_indicators():
    data = pd.DataFrame({
        'Close': [100, 101, 102, 103, 104] * 10,
        'Timestamp': pd.date_range(start='2023-01-01', periods=50, freq='D')
    })
    mock_news = [
        {'title': 'Company achieves record-breaking profits!', 'date': '2023-01-01'},
        {'title': 'Company suffers massive financial loss', 'date': '2023-01-02'},
        {'title': 'Market shows no significant change', 'date': '2023-01-03'}
    ]
    
    # 測試基本技術指標
    result = add_technical_indicators(data)
    assert 'SMA_50' in result.columns
    assert 'RSI_14' in result.columns
    assert len(result) == len(data)
    
    # 測試加上新聞情緒
    result_with_news = add_technical_indicators(data, news_data=mock_news)
    assert 'sentiment' in result_with_news.columns
    assert result_with_news['sentiment'].iloc[0] > 0  # 正向新聞
    assert result_with_news['sentiment'].iloc[1] < 0  # 負向新聞
    assert result_with_news['sentiment'].iloc[2] == 0  # 中性新聞