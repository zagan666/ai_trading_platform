# dashboard.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import asyncio
import os

# 導入我們自己建立的所有模組
from data.data_handler import fetch_data
from data.real_time_data import get_real_time_data
from core.feature_engineering import add_technical_indicators
from strategies.base_strategy import BaseStrategy
from strategies.strategy import MovingAverageCrossoverStrategy
from strategies.ai_strategy import AIStrategy
from core.backtester import Backtester
from core.real_time_engine import RealTimeEngine
from core.paper_trader import PaperTrader
from strategies.custom_strategy_loader import load_custom_strategies

# --- Streamlit 網頁介面設定 ---
st.set_page_config(layout="wide")
st.title("AI Trading Platform")

# --- 載入自訂策略 ---
custom_strategies = load_custom_strategies('custom_strategies')

# --- 側邊欄參數輸入 ---
st.sidebar.header("Mode Selection")
mode = st.sidebar.radio("Select Mode", ["Backtest (Historical)", "Simulation (Real-Time)"])

if mode == "Backtest (Historical)":
    st.sidebar.header("Backtest Parameters")
    ticker = st.sidebar.text_input("Ticker", "SPY")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))
    initial_capital = st.sidebar.number_input("Initial Capital", min_value=1000, value=10000)
    
    # 策略選項：標準 + 自訂
    strategy_options = ["ma_crossover", "ai_strategy"] + list(custom_strategies.keys())
    strategy_name = st.sidebar.selectbox("Strategy", strategy_options)

    if st.sidebar.button("Run Backtest"):
        with st.spinner("Running backtest..."):
            try:
                raw_data = fetch_data(ticker, start_date, end_date)
                strategy: BaseStrategy
                data_for_backtest: pd.DataFrame

                if strategy_name in custom_strategies:
                    strategy = custom_strategies[strategy_name]()  # 實例化自訂策略
                    data_for_backtest = raw_data
                elif strategy_name == "ma_crossover":
                    strategy = MovingAverageCrossoverStrategy(fast_window=50, slow_window=200)
                    data_for_backtest = raw_data
                elif strategy_name == "ai_strategy":
                    MODEL_PATH = 'models/xgboost_model_v1.joblib'
                    strategy = AIStrategy(model_path=MODEL_PATH)
                    data_for_backtest = add_technical_indicators(raw_data)

                backtester = Backtester(initial_capital=initial_capital, strategy=strategy)
                performance_df = backtester.run(data_for_backtest)

                st.subheader(f"Performance Chart: {strategy_name.replace('_', ' ').title()}")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=performance_df.index, y=performance_df['strategy'], mode='lines', name='Strategy'))
                fig.add_trace(go.Scatter(x=performance_df.index, y=performance_df['benchmark'], mode='lines', name='Benchmark'))
                fig.update_layout(title=f'{ticker} Performance', xaxis_title='Date', yaxis_title='Portfolio Value')
                st.plotly_chart(fig, use_container_width=True)

                final_strategy_value = performance_df['strategy'].iloc[-1]
                final_benchmark_value = performance_df['benchmark'].iloc[-1]
                strategy_return = (final_strategy_value / initial_capital - 1) * 100
                benchmark_return = (final_benchmark_value / initial_capital - 1) * 100

                col1, col2 = st.columns(2)
                col1.metric("Strategy Final Value", f"${final_strategy_value:,.2f}", f"{strategy_return:.2f}%")
                col2.metric("Benchmark Final Value", f"${final_benchmark_value:,.2f}", f"{benchmark_return:.2f}%")

            except Exception as e:
                st.error(f"An error occurred: {e}")

else:  # Real-Time Simulation Mode
    st.sidebar.header("Simulation Parameters")
    exchange = st.sidebar.text_input("Exchange", "binance")
    symbol = st.sidebar.text_input("Symbol", "BTC/USDT")
    # 策略選項：標準 + 自訂
    strategy_options = ["ma_crossover", "ai_strategy"] + list(custom_strategies.keys())
    strategy_name = st.sidebar.selectbox("Strategy", strategy_options)
    initial_capital = st.sidebar.number_input("Initial Capital", min_value=1000, value=10000)
    refresh_interval = st.sidebar.number_input("Refresh Interval (seconds)", min_value=1, value=60)

    if st.sidebar.button("Start Simulation"):
        st.subheader("Real-Time Simulation Running...")
        placeholder = st.empty()

        async def run_simulation():
            trader = PaperTrader(initial_capital=initial_capital)
            strategy: BaseStrategy
            if strategy_name in custom_strategies:
                strategy = custom_strategies[strategy_name]()  # 實例化自訂策略
            elif strategy_name == "ai_strategy":
                MODEL_PATH = 'models/xgboost_model_v1.joblib'
                strategy = AIStrategy(model_path=MODEL_PATH)
            else:
                strategy = MovingAverageCrossoverStrategy(fast_window=50, slow_window=200)

            engine = RealTimeEngine(strategy=strategy)

            while True:
                data = await get_real_time_data(exchange, symbol, limit=1)
                if strategy_name == "ai_strategy":
                    data = add_technical_indicators(data)
                events = await engine.process_data(data)
                for event in events:
                    await trader.process_event(event)

                # 更新儀表板顯示 (修正 'close' 為 'Close')
                placeholder.text(f"Current Cash: {trader.cash:.2f} | Position: {trader.position:.4f} | Price: {data['Close'].iloc[-1]:.2f}")
                await asyncio.sleep(refresh_interval)

        asyncio.run(run_simulation())

    else:
        st.info("Set parameters and click 'Start Simulation'.")