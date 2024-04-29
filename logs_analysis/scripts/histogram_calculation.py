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

mean_value = df['Processing Time (s)'].mean()
sns.set(style="whitegrid")


n, bins, patches = plt.hist(df['Processing Time (s)'], color='skyblue', edgecolor='black', bins=15)  # Vous pouvez ajuster le nombre de bins selon vos données

plt.axvline(df['Processing Time (s)'].mean(),linestyle='--', linewidth=3, color='red', label="Temps moyen de transcription")

# Ajouter des titres et des étiquettes avec une meilleure mise en forme
plt.title('Histogramme de temps de transcription', fontsize=25, fontweight='bold')
plt.xlabel('Temps de traitement en secondes', fontsize=20)
plt.ylabel("Nombre d'occurence", fontsize=20)

# Afficher le grille de fond
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
max_height = max(n)  # Obtenir la hauteur maximale des barres de l'histogramme
annot_height = max_height * 0.9  # Placer le texte à 90% de la hauteur maximale

# Annoter la valeur de la moyenne
plt.text(mean_value+0.01, annot_height, f'{mean_value:.2f} s', color='red', fontsize=16)
plt.legend(fontsize=16)
# Afficher le graphique
plt.show()
