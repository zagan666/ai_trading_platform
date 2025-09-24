import pytest
from strategies.custom_strategy_loader import load_custom_strategies
from strategies.base_strategy import BaseStrategy  # 新增這行

@pytest.fixture
def custom_strategy_dir(tmpdir):
    # 建立臨時資料夾模擬 custom_strategies
    dir = tmpdir.mkdir("custom_strategies")
    file = dir.join("my_strategy.py")
    file.write("""
from strategies.base_strategy import BaseStrategy
import pandas as pd

class MyCustomStrategy(BaseStrategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals_df = data.copy()
        signals_df['signal'] = 'HOLD'
        return signals_df
""")
    return str(dir)

def test_load_custom_strategies(custom_strategy_dir):
    # 1. 準備
    # 執行
    custom_strategies = load_custom_strategies(custom_strategy_dir)

    # 3. 斷言
    assert 'MyCustomStrategy' in custom_strategies
    assert issubclass(custom_strategies['MyCustomStrategy'], BaseStrategy)