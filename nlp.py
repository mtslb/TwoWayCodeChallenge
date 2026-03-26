import pandas as pd
import re
import time
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('punkt_tab')
from config import INSTRUMENTS_MAP, UNITS_MULTIPLIER, SIDE_MAP

# Téléchargement des ressources minimales (une seule fois)
nltk.download('punkt', quiet=True)

def extract_financial_data(msg):
    # Nettoyage et Tokenisation
    tokens = word_tokenize(msg.upper())
    
    amount, price = None, None
    detected_sides = set()
    
    # 1. Détection de la Direction (Buy / Sell / Two-Way)
    for side, keywords in SIDE_MAP.items():
        if any(kw.upper() in tokens for kw in keywords):
            detected_sides.add(side)
    
    direction = "NONE"
    if len(detected_sides) > 1: direction = "TWO_WAY"
    elif len(detected_sides) == 1: direction = list(detected_sides)[0]

    # 2. Distinction Amount vs Price
    # On parcourt les tokens pour trouver les nombres
    for i, token in enumerate(tokens):
        # Nettoyage du token pour vérifier s'il est numérique (ex: "1,200.50")
        clean_token = token.replace(',', '')
        
        if re.match(r'^\d+(\.\d+)?$', clean_token):
            val = float(clean_token)
            
            # --- LOGIQUE DE CONTEXTE ---
            # On regarde le mot juste AVANT le nombre
            prev_word = tokens[i-1] if i > 0 else ""
            
            # Si précédé de indicateurs de prix, c'est un PRIX
            if prev_word in ['AT', '@', 'LEVEL', 'REF', 'PRICE']:
                price = val
            # Si c'est un gros chiffre sans indicateur, ou le premier chiffre rencontré
            elif amount is None:
                amount = val
            # Si on a déjà un montant mais pas de prix, le second chiffre est souvent le prix
            elif price is None:
                price = val

    # 3. Correction Amount avec multiplicateurs (K, M, B)
    # On utilise Regex sur le message brut pour ne pas rater "10M" collé
    unit_pattern = r'(\d+(?:\.\d+)?)\s?(' + '|'.join(UNITS_MULTIPLIER.keys()) + r')\b'
    match = re.search(unit_pattern, msg, re.IGNORE_CASE)
    if match:
        amount = float(match.group(1)) * UNITS_MULTIPLIER.get(match.group(2).upper(), 1)

    return amount, price, direction

def process_row(row):
    start_time = time.perf_counter()
    msg = str(row['message'])
    
    res = {
        'Product': None, 'Instrument': None, 'Amount': None, 
        'Price': None, 'Direction': 'NONE', 'Duration_ms': 0
    }

    # Extraction des données financières
    res['Amount'], res['Price'], res['Direction'] = extract_financial_data(msg)

    # Mapping Instrument & Product
    msg_upper = msg.upper()
    for prod, tickers in INSTRUMENTS_MAP.items():
        for t in tickers:
            if re.search(rf'\b{t}\b', msg_upper):
                res['Instrument'], res['Product'] = t, prod
                break
        if res['Instrument']: break
    
    res['Duration_ms'] = (time.perf_counter() - start_time) * 1000
    return pd.Series(res)

# --- EXECUTION ---
df = pd.read_csv('messages.csv')
df_enriched = df.apply(process_row, axis=1)
df = pd.concat([df, df_enriched], axis=1)
df['message'] = df['message'].astype(str).str.upper()


df.to_csv('messages_enriched_2.csv', index=False)
print(f"Terminé. Direction détectée et Distinction Prix/Montant appliquée.")