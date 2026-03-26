# config.py

# Dictionnaire des instruments par classe d'actifs
# Note : On inclut les tickers officiels et le "slang" de marché
INSTRUMENTS_MAP = {
    'FX': [
        'USDCAD', 'EURUSD', 'GBPUSD', 'USDJPY', 'EURGBP', 'AUDUSD', 'EURJPY', 'USDCHF',
        'CABLE', 'GUY', 'LOONIE', 'SWISSY', 'FIBO', 'KIWI', 'MATI', 'STIR'
    ],
    'EQUITY': [
        'META', 'AAPL', 'TSLA', 'MSFT', 'NVIDIA', 'GOOGL', 'AMZN', 'NFLX', 'AMD', 
        'INTC', 'PYPL', 'BABA', 'V', 'MA', 'DIS', 'BA', 'JPM', 'GS'
        'MC.PA', 'OR.PA', 'ASML.AS', 'SAP.DE', 'SIE.DE', 'SAN.MC', 'BP.L', 'VOD.L'
    ],
    'INDICES': [
        'SPX', 'SPY', 'NDX', 'QQQ', 'VIX', 'DAX', 'CAC40', 'FTSE', 'NI225', 'HSI', 'SX5E'
    ],
    'BONDS': [
        'UST', 'BUND', 'GILT', 'OAT', 'BTPS', 'BONOS', 'JGB', 'T-NOTE', 'T-BILL'
    ],
    'COMMODITIES': [
        'XAUUSD', 'GOLD', 'XAGUSD', 'SILVER', 'WTI', 'BRENT', 'NG', 'COPPER'
    ],
    'CRYPTO': [
        'BTC', 'ETH', 'SOL', 'XRP', 'DOT', 'ADA', 'LINK'
    ]
}

# Lexique des unités (pour la conversion de l'Amount)
UNITS_MULTIPLIER = {
    'K': 1_000,
    'M': 1_000_000,
    'MIO': 1_000_000,
    'MIO.': 1_000_000,
    'MLN': 1_000_000,
    'BUCKS': 1_000_000,      # Slang pour 1M$
    'YARD': 1_000_000_000,   # Slang pour 1 Milliard
    'BILLION': 1_000_000_000,
    'B': 1_000_000_000
}

# Mots-clés pour détecter le SENS (Optionnel mais recommandé)
SIDE_MAP = {
    'BUY': ['BUY', 'BID', 'BOT', 'TAKE', 'LIFT', 'MINE'],
    'SELL': ['SELL', 'OFFER', 'ASK', 'SOLD', 'HIT', 'YOURS']
}

