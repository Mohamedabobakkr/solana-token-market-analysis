import requests
import logging
import colorama
from colorama import Fore, Style
import time
import os
from datetime import datetime
from tabulate import tabulate
from config import *
from data_manager import DataManager
from analyzer import TokenAnalyzer

# Initialize colorama for colored output
colorama.init()

# Configure logging
logging.basicConfig(
    filename='logs/market_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_top_solana_tokens():
    """Fetch token data from Jupiter API"""
    try:
        print(f"{Fore.YELLOW}Fetching Solana data...{Style.RESET_ALL}")
        
        # Use Jupiter API
        url = f"https://price.jup.ag/v4/price?ids={TOKENS_TO_TRACK}"
        response = requests.get(url)
        
        print(f"API Response Status: {response.status_code}")
        data = response.json()
        
        if 'data' not in data:
            print(f"{Fore.RED}No data field in response{Style.RESET_ALL}")
            return None
            
        tokens = []
        for token_id, token_data in data['data'].items():
            try:
                if 'price' in token_data:
                    token = {
                        'symbol': token_id,
                        'price': float(token_data['price']),
                        'change_24h': float(token_data.get('price_24h_change', 0)),
                        'volume_24h': float(token_data.get('volume_24h', 0))
                    }
                    tokens.append(token)
            except Exception as e:
                print(f"Error processing {token_id}: {e}")
                continue
        
        if tokens:
            # Sort tokens
            volume_sorted = sorted(tokens, key=lambda x: x['volume_24h'], reverse=True)
            change_sorted = sorted(tokens, key=lambda x: x['change_24h'], reverse=True)
            
            return {
                'all_tokens': volume_sorted,  # Changed this line
                'top_gainers': change_sorted[:3],
                'top_losers': change_sorted[-3:]
            }
        
        return None
        
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        logging.error(f"Error fetching Solana tokens: {str(e)}")
        return None

def format_price(price):
    """Format price with appropriate decimal places"""
    if price is None:
        return "N/A"
    price = float(price)
    if price < 0.01:
        return f"${price:.8f}"
    elif price < 1:
        return f"${price:.4f}"
    else:
        return f"${price:.2f}"

def format_change(change):
    """Format price change with colors"""
    if change is None:
        return "N/A"
    change = float(change)
    if change > 5:
        return f"{Fore.GREEN}↑↑ +{change:.2f}%{Style.RESET_ALL}"
    elif change > 0:
        return f"{Fore.GREEN}↑ +{change:.2f}%{Style.RESET_ALL}"
    elif change < -5:
        return f"{Fore.RED}↓↓ {change:.2f}%{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}↓ {change:.2f}%{Style.RESET_ALL}"

def display_token_table(tokens, title):
    """Display token data in a formatted table"""
    print(f"\n{Fore.YELLOW}{title}:{Style.RESET_ALL}")
    headers = ['Symbol', 'Price', '24h Change', 'Volume']
    table_data = []
    
    for token in tokens:
        table_data.append([
            token['symbol'],
            format_price(token['price']),
            format_change(token['change_24h']),
            f"${float(token.get('volume_24h', 0)):,.0f}"
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt='grid'))

def check_price_alerts(tokens, alerts):
    """Check for price movements that trigger alerts"""
    triggered = []
    for token in tokens:
        change = float(token.get('change_24h', 0))
        if abs(change) >= alerts.get('price_change', 5):
            triggered.append({
                'symbol': token['symbol'],
                'change': change,
                'price': token['price']
            })
    return triggered


def main():
    # Initialize components
    data_manager = DataManager(DATA_FILE)
    analyzer = TokenAnalyzer(data_manager)
    
    while True:
        try:
            os.system('cls')
            print(f"{Fore.CYAN}=== Solana Market Analysis Dashboard ==={Style.RESET_ALL}")
            
            # Fetch and save token data
            tokens = get_top_solana_tokens()
            if tokens:
                data_manager.save_token_data(tokens)
                
                # Display current prices
                display_token_table(tokens['all_tokens'], 'Current Prices')
                
                # Display analysis
                print(f"\n{Fore.YELLOW}24h Analysis:{Style.RESET_ALL}")
                for token in tokens['all_tokens']:
                    volatility = analyzer.calculate_volatility(token['symbol'])
                    trend = analyzer.get_price_trends(token['symbol'])
                    if volatility:
                        print(f"{token['symbol']}: Volatility: {volatility:.2f}% | Trend: {trend}")
                
                # Display gainers and losers
                display_token_table(tokens['top_gainers'], 'Top Gainers')
                display_token_table(tokens['top_losers'], 'Top Losers')
            
            print(f"\n{Fore.CYAN}Press Ctrl+C to exit. Refreshing in {REFRESH_RATE} seconds...{Style.RESET_ALL}")
            time.sleep(REFRESH_RATE)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
            time.sleep(5)
            continue
if __name__ == "__main__":
    main()        