# tests/test_ai_strategy.py
import pandas as pd
import pytest
import os

# 這是我們即將要建立的新策略類別
from strategies.ai_strategy import AIStrategy

# 確保模型檔案存在，如果不存在則跳過此測試
MODEL_PATH = 'models/xgboost_model_v1.joblib'
pytestmark = pytest.mark.skipif(not os.path.exists(MODEL_PATH), reason="Model file not found")

@pytest.fixture
def sample_feature_data():
    """提供一個包含模型所需特徵的假數據。"""
    return pd.DataFrame({
        'SMA_50': [200, 201, 202],
        'RSI_14': [50, 60, 70]
    })

def test_ai_strategy_generates_signals(sample_feature_data):
    # 1. 準備 (Arrange)
    strategy = AIStrategy(model_path=MODEL_PATH)

    # 2. 執行 (Act)
    signals_df = strategy.generate_signals(sample_feature_data)

    # 3. 斷言 (Assert)
    # 斷言 'signal' 欄位存在
    assert 'signal' in signals_df.columns

    # 斷言信號的值都在我們預期的集合中
    expected_signals = {'BUY', 'SELL', 'HOLD'}
    assert set(signals_df['signal'].unique()).issubset(expected_signals)