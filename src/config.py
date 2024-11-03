# Token settings
TOKENS_TO_TRACK = (
    "SOL,JUP,BONK,POPCAT,WIF,JITO,ORCA,TENSOR,"
    "PYTH,MSOL,BOME,W,CROWN,RLB,HADES,"
    "SAMO,GUAC,FORGE,USDC"
)

# Display names and descriptions (optional, for future use)
TOKEN_INFO = {
    "SOL": "Solana",
    "JUP": "Jupiter",
    "BONK": "Bonk",
    "POPCAT": "Popcat",
    "WIF": "Woof",
    "JTO": "Jito",
    "ORCA": "Orca",
    "TENSOR": "Tensor",
    "PYTH": "Pyth Network",
    "MSOL": "Marinade SOL",
    "BOME": "Book of Meme",
    "W": "Wormhole",
    "CROWN": "Crown Token",
    "RLB": "Rollbit",
    "HADES": "Hades",
    "SAMO": "Samoyedcoin",
    "GUAC": "Guacamole",
    "FORGE": "Forge",
    "USDC": "USD Coin"
}

# Refresh rate and alert threshold
REFRESH_RATE = 30  # seconds
ALERT_THRESHOLD = 3  # percentage

# Display settings
DISPLAY_TOP_N = 5  # number of tokens to show in each category
CHART_WIDTH = 50  # for ASCII charts

# File paths
LOG_FILE = "logs/market_analysis.log"
DATA_FILE = "data/token_history.json"