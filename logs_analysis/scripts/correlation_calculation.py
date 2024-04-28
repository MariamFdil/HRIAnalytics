import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Correlation calculation.")
parser.add_argument('file_path', type=str, help='The path to the CSV file.')
args = parser.parse_args()

# Charger les données
df = pd.read_csv(args.file_path)

# Prétraitement - calculer la longueur de la phrase en nombre de caractères
df['Text Length'] = df['Text'].apply(len)

# Analyse de corrélation
correlation = df['Processing Time (s)'].corr(df['Text Length'])
print(f"La corrélation entre la longueur du texte et le temps de traitement est : {correlation}")

# Visualisation
plt.figure(figsize=(12, 6))  # TODO : ajustement de la taille du graphique
sns.scatterplot(data=df, x='Text Length', y='Processing Time (s)', s=100)  # TODO : ajustement taille de points
plt.title('Relation entre la Longueur de la Phrase et le Temps de Traitement', fontsize=16)
plt.xlabel('Longueur du Texte (nombre de caractères)', fontsize=14)
plt.ylabel('Temps de Traitement (s)', fontsize=14)
plt.grid(True) 

# Ligne de régression
sns.regplot(data=df, x='Text Length', y='Processing Time (s)', scatter=False, color='red')

plt.show()

