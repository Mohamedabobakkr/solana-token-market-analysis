import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.ensure_data_dir()
        
    def ensure_data_dir(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
    def save_token_data(self, tokens):
        """Save token data with timestamp"""
        timestamp = datetime.now().isoformat()
        data_to_save = {
            'timestamp': timestamp,
            'tokens': tokens
        }
        
        try:
            # Load existing data
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
                
            # Add new data
            history.append(data_to_save)
            
            # Keep only last 24 hours of data
            one_day_ago = datetime.now().timestamp() - (24 * 60 * 60)
            history = [
                h for h in history 
                if datetime.fromisoformat(h['timestamp']).timestamp() > one_day_ago
            ]
            
            # Save updated history
            with open(self.data_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"Error saving data: {e}")