# strategies/ai_strategy.py
import pandas as pd
import joblib
from .base_strategy import BaseStrategy

class AIStrategy(BaseStrategy):
    """
    使用預先訓練好的機器學習模型來產生交易信號的策略。
    """
    def __init__(self, model_path: str):
        """
        初始化 AI 策略，並載入訓練好的模型。

        Args:
            model_path (str): 已儲存的模型檔案的路徑 (例如 .joblib 檔案)。
        """
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            print(f"Error: Model file not found at {model_path}")
            self.model = None

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        使用載入的模型，對包含特徵的數據進行預測，並產生信號。

        Args:
            data (pd.DataFrame): 必須包含模型訓練時使用的所有特徵欄位。

        Returns:
            pd.DataFrame: 增加了 'signal' 欄位的 DataFrame。
        """
        if self.model is None:
            raise RuntimeError("Model is not loaded. Cannot generate signals.")

        # 複製數據以避免修改原始 DataFrame
        signals_df = data.copy()

        # 確保數據中包含模型需要的所有特徵欄位
        required_features = self.model.feature_names_in_
        if not all(feature in signals_df.columns for feature in required_features):
            raise ValueError(f"Input data is missing required features. Model needs: {required_features}")

        # 1. 使用模型進行預測 (結果是 0 或 1)
        predictions = self.model.predict(signals_df[required_features])

        # 2. 將模型的預測 (0 或 1) 轉換為我們系統的信號 ('BUY', 'SELL', 'HOLD')
        #    - 預測為 1 (上漲)，信號為 BUY
        #    - 預測為 0 (下跌/持平)，我們在這裡定義為 SELL/出場信號
        #    - 您也可以定義成 HOLD，取決於策略設計
        signals_df['signal'] = ['BUY' if pred == 1 else 'SELL' for pred in predictions]

        return signals_df