import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Chargement des données nettoyées (créées à l'étape précédente)
df = pd.read_csv('market_data_cleaned.csv', index_col=0, parse_dates=True)

# 2. Construction de l'indicateur Macro
# On calcule la Moyenne Mobile Simple (SMA) sur 50 jours des taux US
df['US_Rate_SMA_50'] = df['US_10Y_Rate'].rolling(window=50).mean()

# 3. Génération du Signal (La "Règle de Trading")
# Si Taux Actuel > Moyenne 50 jours -> Tendance Taux Haussière -> Dollar Fort -> VENDRE EUR/USD (-1)
# Sinon -> ACHETER EUR/USD (1)
df['Signal'] = np.where(df['US_10Y_Rate'] > df['US_Rate_SMA_50'], -1, 1)

# On décale le signal d'un jour (shift) car on ne peut trader qu'après la clôture du marché
# C'est crucial pour éviter le "Look-ahead bias" (tricher en connaissant le futur)
df['Signal'] = df['Signal'].shift(1)

# 4. Visualisation de la stratégie
plt.figure(figsize=(14, 7))

# On trace le prix de l'EUR/USD
plt.plot(df.index, df['EUR_USD'], label='EUR/USD Price', color='black', alpha=0.6)

# On colorie le fond du graphique selon le signal
# Vert = On est Long (Achat)
# Rouge = On est Short (Vente)
y_min, y_max = df['EUR_USD'].min(), df['EUR_USD'].max()
plt.fill_between(df.index, y_min, y_max, where=(df['Signal'] == 1), color='green', alpha=0.1, label='Long Signal (Weak US Rates)')
plt.fill_between(df.index, y_min, y_max, where=(df['Signal'] == -1), color='red', alpha=0.1, label='Short Signal (Strong US Rates)')

plt.title('Stratégie Algo : Signaux basés sur le Trend des Taux US')
plt.legend(loc='upper left')
plt.show()

# 5. Sauvegarde pour l'étape de Backtest
df.to_csv('market_data_with_signal.csv')
print("Signaux générés et sauvegardés dans 'market_data_with_signal.csv'")