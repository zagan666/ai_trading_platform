# data/real_time_data.py
import ccxt.async_support as ccxt_async
import pandas as pd
import asyncio

async def get_real_time_data(exchange_name: str, symbol: str, limit: int = 10) -> pd.DataFrame:
    exchange = getattr(ccxt_async, exchange_name)()
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe='1m', limit=limit)
    finally:
        await exchange.close()
    
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    data = pd.DataFrame(ohlcv, columns=columns)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    return data