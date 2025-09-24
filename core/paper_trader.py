# core/paper_trader.py
import asyncio

class PaperTrader:
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.position = 0.0  # 持倉數量

    async def process_event(self, event):
        if event['type'] == 'signal':
            signal = event['signal']
            price = event['price']
            
            if signal == 'BUY' and self.cash > 0:
                self.position = self.cash / price
                self.cash = 0.0
            
            elif signal == 'SELL' and self.position > 0:
                self.cash = self.position * price
                self.position = 0.0