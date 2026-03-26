import pandas as pd
import re
import time
from config import INSTRUMENTS_MAP, UNITS_MULTIPLIER

# 1. Chargement et Normalisation
df = pd.read_csv('messages.csv')
df['message'] = df['message'].astype(str).str.upper()

def process_row(row):
    start_time = time.perf_counter() # Timestamp de début (précision nanoseconde)
    
    msg = row['message']
    channel = row['channel']
    
    # Valeurs par défaut
    found_prod, found_inst, amount, price = None, None, None, None
    
    if channel == 'broker-chat':
        # --- Extraction Instrument ---
        for product, tickers in INSTRUMENTS_MAP.items():
            for t in tickers:
                if re.search(rf'\b{t}\b', msg):
                    found_inst, found_prod = t, product
                    break
            if found_inst: break

        # --- Extraction Prix ---
        price_match = re.search(r'(?:AT|@)\s?(\d+(?:\.\d+)?)\b', msg)
        price = float(price_match.group(1)) if price_match else None

        # --- Extraction Quantité ---
        unit_pattern = r'(\d+(?:\.\d+)?)\s?(' + '|'.join(UNITS_MULTIPLIER.keys()) + r')\b'
        amount_match = re.search(unit_pattern, msg)
        
        if amount_match:
            val = float(amount_match.group(1))
            amount = val * UNITS_MULTIPLIER.get(amount_match.group(2), 1)
        else:
            numbers = re.findall(r'\b\d+(?:\.\d+)?\b', msg)
            for n in numbers:
                n_float = float(n)
                if price is None or n_float != price:
                    amount = n_float
                    break
    
    end_time = time.perf_counter()
    duration = (end_time - start_time) * 1000 # Conversion en millisecondes
    
    return pd.Series([found_prod, found_inst, amount, price, duration])

# 2. Application et création des colonnes
# On ajoute une colonne 'Processing_Time_ms'
df[['Product', 'Instrument', 'Amount', 'Price', 'Processing_Time_ms']] = df.apply(process_row, axis=1)

# 3. Statistiques de performance
avg_time = df[df['channel'] == 'broker-chat']['Processing_Time_ms'].mean()
print(f"Temps moyen de traitement par message broker : {avg_time:.4f} ms")

# 4. Génération du nouveau CSV
df.to_csv('messages_enriched.csv', index=False)
print("Fichier 'messages_enriched.csv' généré avec succès.")