# strategies/base_strategy.py

from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """
    所有策略類的抽象基底 (Abstract Base Class)。

    它定義了所有策略都必須遵守的標準介面 (Interface)，
    也就是說，任何繼承自 BaseStrategy 的類別，
    都必須要實現一個名為 generate_signals 的方法。
    """

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        產生交易信號的核心方法。

        Args:
            data (pd.DataFrame): 包含價格數據的 DataFrame。

        Returns:
            pd.DataFrame: 增加了 'signal' 欄位的 DataFrame。
        """
        pass