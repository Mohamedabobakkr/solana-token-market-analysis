import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from config import *
from data_manager import DataManager
from analyzer import TokenAnalyzer
from visualizer import TokenVisualizer

def get_top_solana_tokens():
    """Fetch token data from Jupiter API"""
    try:
        url = f"https://price.jup.ag/v4/price?ids={TOKENS_TO_TRACK}"
        response = requests.get(url)
        data = response.json()
        
        if 'data' not in data:
            st.error("No data received from API")
            return None
            
        tokens = []
        for token_id, token_data in data['data'].items():
            if 'price' in token_data:
                token = {
                    'symbol': token_id,
                    'price': float(token_data['price']),
                    'change_24h': float(token_data.get('price_24h_change', 0)),
                    'volume_24h': float(token_data.get('volume_24h', 0))
                }
                tokens.append(token)
        
        if tokens:
            volume_sorted = sorted(tokens, key=lambda x: x['volume_24h'], reverse=True)
            change_sorted = sorted(tokens, key=lambda x: x['change_24h'], reverse=True)
            
            return {
                'all_tokens': volume_sorted,
                'top_gainers': change_sorted[:3],
                'top_losers': change_sorted[-3:]
            }
        
        return None
        
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Solana Market Analysis", layout="wide")
    
    # Initialize components
    data_manager = DataManager(DATA_FILE)
    analyzer = TokenAnalyzer(data_manager)
    visualizer = TokenVisualizer(data_manager)
    
    # Header
    st.title("Solana Market Analysis Dashboard")
    
    # Fetch current data
    tokens = get_top_solana_tokens()
    
    if tokens:
        # Save token data
        data_manager.save_token_data(tokens)
        
        # Create three columns for metrics
        col1, col2, col3 = st.columns(3)
        
        # Display total volume
        total_volume = sum(token['volume_24h'] for token in tokens['all_tokens'])
        col1.metric("Total 24h Volume", f"${total_volume:,.0f}")
        
        # Display number of tokens tracked
        col2.metric("Tokens Tracked", len(tokens['all_tokens']))
        
        # Display average change
        avg_change = sum(token['change_24h'] for token in tokens['all_tokens']) / len(tokens['all_tokens'])
        col3.metric("Average 24h Change", f"{avg_change:.2f}%")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Current Prices", "Top Movers", "Analysis"])
        
        with tab1:
            # Current Prices Table
            df = pd.DataFrame(tokens['all_tokens'])
            st.dataframe(
                df.style.format({
                    'price': '${:.4f}',
                    'change_24h': '{:.2f}%',
                    'volume_24h': '${:,.0f}'
                }),
                use_container_width=True
            )
            
            # Price Chart
            selected_token = st.selectbox(
                "Select token for price history",
                [token['symbol'] for token in tokens['all_tokens']]
            )
            fig = visualizer.plot_price_history(selected_token)
            if fig:
                st.pyplot(fig)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Gainers")
                st.dataframe(
                    pd.DataFrame(tokens['top_gainers']).style.format({
                        'price': '${:.4f}',
                        'change_24h': '{:.2f}%',
                        'volume_24h': '${:,.0f}'
                    })
                )
            
            with col2:
                st.subheader("Top Losers")
                st.dataframe(
                    pd.DataFrame(tokens['top_losers']).style.format({
                        'price': '${:.4f}',
                        'change_24h': '{:.2f}%',
                        'volume_24h': '${:,.0f}'
                    })
                )
        
# ... existing code ...

        with tab3:
            st.subheader("Token Analysis")
            for token in tokens['all_tokens']:
                with st.expander(f"{token['symbol']} Analysis"):
                    volatility = analyzer.calculate_volatility(token['symbol'])
                    trend = analyzer.get_price_trends(token['symbol'])
                    col1, col2 = st.columns(2)
                    
                    # Add null checks
                    volatility_display = f"{volatility:.2f}%" if volatility is not None else "N/A"
                    trend_display = trend if trend is not None else "N/A"
                    
                    col1.metric("Volatility", volatility_display)
                    col2.metric("Trend", trend_display)

     
        # Auto-refresh
        st.empty()
        st.button("Refresh Data")

if __name__ == "__main__":
    main()