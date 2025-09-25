import pandas as pd
from transformers import pipeline

def add_news_sentiment(data: pd.DataFrame, news_data: list) -> pd.DataFrame:
    # 初始化 FinBERT 情緒分析模型
    sentiment_analyzer = pipeline('sentiment-analysis', model='yiyanghkust/finbert-tone')
    
    # 複製數據
    result = data.copy()
    result['sentiment'] = 0.0
    
    # 對每條新聞進行情緒分析並匹配日期
    for news in news_data:
        date = news['date']
        title = news['title']
        sentiment = sentiment_analyzer(title)[0]
        print(f"News: {title}, Sentiment: {sentiment}")  # 除錯用
        
        # 將情緒轉為連續數值：正向 (0 到 1)，負向 (-1 到 0)，中性 (0)
        sentiment_score = (
            sentiment['score'] if sentiment['label'].lower() == 'positive' else
            -sentiment['score'] if sentiment['label'].lower() == 'negative' else
            0.0
        )
        
        # 匹配日期（確保格式一致）
        date = pd.to_datetime(date).strftime('%Y-%m-%d')
        result['Timestamp'] = pd.to_datetime(result['Timestamp']).dt.strftime('%Y-%m-%d')
        if date in result['Timestamp'].values:
            result.loc[result['Timestamp'] == date, 'sentiment'] = sentiment_score
    
    return result