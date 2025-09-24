# core/real_time_engine.py
import asyncio
from strategies.base_strategy import BaseStrategy

class RealTimeEngine:
    def __init__(self, strategy: BaseStrategy = None):
        self.strategy = strategy

    async def process_data(self, data):
        # 模擬事件流: 從數據產生市場事件
        events = [{'type': 'market_update', 'data': row} for index, row in data.iterrows()]

        # 如果有策略，產生信號事件
        if self.strategy:
            signals_df = self.strategy.generate_signals(data)
            for index, row in signals_df.iterrows():
                events.append({'type': 'signal', 'signal': row['signal'], 'price': row['close']})

        return events