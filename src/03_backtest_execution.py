import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- GESTION DES CHEMINS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'market_data_with_signal.csv')

# 1. Chargement des données avec les signaux
if not os.path.exists(csv_path):
    print("⚠️ ERREUR : Lance d'abord l'étape 2 pour créer 'market_data_with_signal.csv'")
    exit()

df = pd.read_csv(csv_path, index_col=0, parse_dates=True)

# 2. Calcul des Rendements (Returns)
# On calcule le rendement quotidien de l'EUR/USD : (Prix J / Prix J-1) - 1
df['Returns'] = df['EUR_USD'].pct_change()

# 3. Calcul de la Performance de la Stratégie
# Strategy Return = Signal (Hier) * Market Return (Aujourd'hui)
# Si j'ai acheté (1) et que le marché monte (+1%) -> Je gagne +1%
# Si j'ai vendu (-1) et que le marché baisse (-1%) -> Je gagne +1% (Short)
df['Strategy_Returns'] = df['Signal'] * df['Returns']

# 4. Calcul de la Courbe de Capital (Cumulative Returns)
# On part d'une base 100
df['Cumulative_Market'] = (1 + df['Returns']).cumprod() * 100
df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod() * 100

# 5. Visualisation Finale "Institutional Grade"
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Cumulative_Strategy'], label='Notre Stratégie Macro', color='green', linewidth=2)
plt.plot(df.index, df['Cumulative_Market'], label='Buy & Hold EUR/USD', color='grey', linestyle='--', alpha=0.6)

plt.title('Backtest: Performance de la Stratégie vs Benchmark')
plt.ylabel('Performance (Base 100)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 6. Statistiques Clés pour le CV
total_return = df['Cumulative_Strategy'].iloc[-1] - 100
annualized_vol = df['Strategy_Returns'].std() * np.sqrt(252) * 100
sharpe_ratio = (df['Strategy_Returns'].mean() / df['Strategy_Returns'].std()) * np.sqrt(252)

print(f"--- RÉSULTATS DU BACKTEST ---")
print(f"Rendement Total : {total_return:.2f}%")
print(f"Volatilité Annualisée : {annualized_vol:.2f}%")
print(f"Ratio de Sharpe : {sharpe_ratio:.2f}")