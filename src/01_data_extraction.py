import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os # Indispensable pour gérer les dossiers

# --- CONFIGURATION AUTOMATIQUE DES CHEMINS ---
# On détecte où se trouve le fichier python
script_dir = os.path.dirname(os.path.abspath(__file__))
# On définit le chemin complet pour le futur fichier CSV
csv_path = os.path.join(script_dir, 'market_data_cleaned.csv')

# 1. Définition des tickers
tickers = ['EURUSD=X', '^TNX'] 

# 2. Téléchargement des données
print("Téléchargement des données en cours...")
try:
    data = yf.download(tickers, start="2020-01-01", end="2024-12-01")['Close']
except KeyError:
    # Au cas où yfinance se met à jour
    data = yf.download(tickers, start="2020-01-01", end="2024-12-01")['Adj Close']

# 3. Nettoyage
df = data.copy()
df = df.dropna()
df.columns = ['EUR_USD', 'US_10Y_Rate']

# 4. Check Visuel rapide
plt.figure(figsize=(10, 5))
plt.plot(df['EUR_USD'], label='EUR/USD')
plt.title("Check Rapide : Données Récupérées")
plt.legend()
plt.show()

# 5. Export Sécurisé
print(f"Sauvegarde en cours vers : {csv_path}")
df.to_csv(csv_path)

print("✅ Succès ! Le fichier CSV est maintenant bien rangé à côté de ton script.")
