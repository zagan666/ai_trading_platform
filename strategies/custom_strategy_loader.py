# strategies/custom_strategy_loader.py
import os
import importlib.util
from .base_strategy import BaseStrategy

def load_custom_strategies(dir_path: str = 'custom_strategies'):
    custom_strategies = {}
    if not os.path.exists(dir_path):
        return custom_strategies
    
    for file in os.listdir(dir_path):
        if file.endswith('.py'):
            module_name = file[:-3]
            module_path = os.path.join(dir_path, file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            for attr in dir(module):
                cls = getattr(module, attr)
                if isinstance(cls, type) and issubclass(cls, BaseStrategy) and cls != BaseStrategy:
                    custom_strategies[attr] = cls
    
    return custom_strategies