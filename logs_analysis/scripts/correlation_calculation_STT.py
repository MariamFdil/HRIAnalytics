import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Correlation calculation.")
parser.add_argument('file_path', type=str, help='The path to the CSV file.')
args = parser.parse_args()

df = pd.read_csv(args.file_path)


sample_rate = 16000
df['Audio Length (s)'] = df['Timestamp (s)'] / sample_rate
print(df['Audio Length (s)'])
correlation = df['Processing Time (s)'].corr(df['Audio Length (s)'])
print(f"La corrélation entre la durée de l'audio et le temps de traitement est : {correlation}")

# Visualisation
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x='Audio Length (s)', y='Processing Time (s)', s=100)
plt.title('Correlation between audio length and transcription time (STT)', fontsize=16)
plt.xlabel('Durée de l\'Audio (secondes)', fontsize=14)
plt.ylabel('Temps de Traitement (s)', fontsize=14)
plt.grid(True) 

sns.regplot(data=df, x='Audio Length (s)', y='Processing Time (s)', scatter=False, color='red')

plt.show()
