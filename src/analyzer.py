import numpy as np
from datetime import datetime, timedelta
import json
class TokenAnalyzer:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        
    def calculate_volatility(self, token_symbol, hours=24):
        """Calculate token volatility over specified hours"""
        try:
            with open(self.data_manager.data_file, 'r') as f:
                history = json.load(f)
                
            prices = []
            for entry in history:
                for token in entry['tokens']['all_tokens']:
                    if token['symbol'] == token_symbol:
                        prices.append(float(token['price']))
            
            if prices:
                returns = np.diff(np.log(prices))
                volatility = np.std(returns) * np.sqrt(24)  # Annualized
                return volatility
            return None
        except Exception as e:
            print(f"Error calculating volatility: {e}")
            return None
            
    def get_price_trends(self, token_symbol):
        """Analyze price trends"""
        try:
            with open(self.data_manager.data_file, 'r') as f:
                history = json.load(f)
            
            prices = []
            timestamps = []
            for entry in history:
                for token in entry['tokens']['all_tokens']:
                    if token['symbol'] == token_symbol:
                        prices.append(float(token['price']))
                        timestamps.append(datetime.fromisoformat(entry['timestamp']))
            
            if len(prices) > 1:
                price_change = ((prices[-1] - prices[0]) / prices[0]) * 100
                direction = "↑" if price_change > 0 else "↓"
                return f"{direction} {abs(price_change):.2f}%"
            return "N/A"
        except Exception as e:
            print(f"Error analyzing trends: {e}")
            return "N/A"