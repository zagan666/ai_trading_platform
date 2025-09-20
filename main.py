# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import Dict, Any

# 導入我們自己建立的所有模組
from data.data_handler import fetch_data
from core.feature_engineering import add_technical_indicators
from strategies.base_strategy import BaseStrategy
from strategies.strategy import MovingAverageCrossoverStrategy
from strategies.ai_strategy import AIStrategy
from core.backtester import Backtester

# --- API Setup ---
app = FastAPI(
    title="AI Trading Platform API",
    description="An API for running trading strategy backtests.",
    version="0.1.0",
)

# --- API Models ---
class StrategyName(str, Enum):
    """可用的策略名稱枚舉"""
    ma_crossover = "ma_crossover"
    ai_strategy = "ai_strategy"

class BacktestRequest(BaseModel):
    """回測請求的資料模型"""
    ticker: str = "SPY"
    start_date: str = "2022-01-01"
    end_date: str = "2023-12-31"
    initial_capital: float = 10000.0
    strategy_name: StrategyName
    
    # 策略的參數 (可選)
    # 這裡我們為了簡化，先寫死在程式碼裡，未來可以從 request 中傳入
    # fast_window: int = 50
    # slow_window: int = 200

# --- API Endpoints ---
@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the AI Trading Platform API"}

@app.post("/backtest")
async def run_backtest(request: BacktestRequest) -> Dict[str, Any]:
    """
    執行交易回測。
    """
    print(f"Received backtest request: {request.dict()}")
    
    try:
        # 1. 獲取原始數據
        raw_data = fetch_data(request.ticker, request.start_date, request.end_date)
        
        strategy: BaseStrategy
        data_for_backtest: pd.DataFrame

        # 2. 根據請求選擇並準備策略和數據
        if request.strategy_name == StrategyName.ma_crossover:
            strategy = MovingAverageCrossoverStrategy(fast_window=50, slow_window=200)
            data_for_backtest = raw_data
        
        elif request.strategy_name == StrategyName.ai_strategy:
            # AI 策略需要特徵數據
            MODEL_PATH = 'models/xgboost_model_v1.joblib'
            strategy = AIStrategy(model_path=MODEL_PATH)
            data_for_backtest = add_technical_indicators(raw_data)
        
        # 3. 執行回測
        backtester = Backtester(initial_capital=request.initial_capital, strategy=strategy)
        result = backtester.run(data_for_backtest)
        
        print(f"Backtest result: {result}")
        return result

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="AI Model file not found.")
    except Exception as e:
        # 捕獲其他所有可能的錯誤
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")