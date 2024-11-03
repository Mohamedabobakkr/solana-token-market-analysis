import matplotlib.pyplot as plt
from datetime import datetime
import json

class TokenVisualizer:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def plot_price_history(self, token_symbol):
        """Plot price history for a given token"""
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
            
            plt.figure(figsize=(10, 6))
            plt.plot(timestamps, prices)
            plt.title(f'{token_symbol} Price History')
            plt.xlabel('Time')
            plt.ylabel('Price (USD)')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            
            return plt
        except Exception as e:
            print(f"Error creating visualization: {e}")
            return None
        