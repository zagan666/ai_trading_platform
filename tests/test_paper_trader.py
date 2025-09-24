# tests/test_paper_trader.py
import pytest
from core.paper_trader import PaperTrader

@pytest.mark.asyncio
async def test_paper_trader():
    # 1. 準備
    trader = PaperTrader(initial_capital=10000.0)
    event = {'type': 'signal', 'signal': 'BUY', 'price': 100.0}

    # 2. 執行
    await trader.process_event(event)

    # 3. 斷言
    assert trader.position > 0  # 已買入
    assert trader.cash == 0.0  # 現金用完