# tests/test_real_time_engine.py
import pytest
from core.real_time_engine import RealTimeEngine
from data.real_time_data import get_real_time_data

@pytest.mark.asyncio
async def test_real_time_engine():
    # 1. 準備
    engine = RealTimeEngine()
    data = await get_real_time_data("binance", "BTC/USDT", 1)  # 取最新一筆

    # 2. 執行
    events = await engine.process_data(data)

    # 3. 斷言
    assert isinstance(events, list)
    assert len(events) > 0
    assert 'type' in events[0]  # 至少有事件類型