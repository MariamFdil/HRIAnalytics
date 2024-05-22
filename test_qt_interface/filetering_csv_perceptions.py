import pandas as pd

# Charger les données depuis un fichier CSV
df = pd.read_csv('/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/perceptions')

# Afficher le nombre initial de lignes pour le diagnostic
print("Nombre initial de lignes :", len(df))

# Vérifier les valeurs uniques dans la colonne 'is_visible'
#print("Valeurs uniques avant transformation :", df['is_visible'].unique())

# Convertir les chaînes de caractères en booléens si nécessaire
df['is_visible'] = df['is_visible'].replace({'True': True, 'False': False})

# Afficher les valeurs uniques après transformation pour vérifier
#print("Valeurs uniques après transformation :", df['is_visible'].unique())

# Assurer que 'is_visible' est une colonne existante et remplacer les valeurs non-booléennes ou manquantes
if 'is_visible' in df.columns:
    # Filtrer pour garder uniquement les lignes où 'is_visible' est True
    df_filtered = df[df['is_visible'] == True]

    # Afficher le nombre de lignes après le filtrage pour le diagnostic
    print("Nombre de lignes après filtrage :", len(df_filtered))

    # Sauvegarder le DataFrame filtré dans un nouveau fichier CSV
    df_filtered.to_csv('/home/introlab/Desktop/Test_TTop_Blanc/Mariam_Fdil/filtred_perceptions.csv', index=False)
    print("Le filtrage est terminé et le fichier filtré est sauvegardé.")
else:
    print("La colonne 'is_visible' n'existe pas dans le fichier CSV.")
